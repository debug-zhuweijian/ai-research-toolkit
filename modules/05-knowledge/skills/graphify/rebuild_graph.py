#!/usr/bin/env python3
"""Batch semantic extraction via OpenAI-compatible API + graphify graph rebuild.

GraphRAG-inspired knowledge graph pipeline:
- LLM-based entity/relationship extraction from document corpus
- Incremental caching (only re-extract changed files)
- Louvain community detection
- Gleaning: multi-round extraction to recover missed entities
- Exponential backoff with full jitter retry

Usage:
    # Set required environment variables
    export GRAPHIFY_API_URL="http://your-llm-endpoint/v1/chat/completions"
    export GRAPHIFY_API_KEY="your-api-key"
    export GRAPHIFY_API_MODEL="your-model-name"

    # Run from the vault root (must contain raw/ directory)
    python rebuild_graph.py

All parameters are configurable via environment variables (see constants below).
"""
import json, os, random, sys, time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# ── Configuration (all overridable via environment variables) ────────────────

API_URL = os.environ.get("GRAPHIFY_API_URL", "")
if not API_URL:
    print("ERROR: GRAPHIFY_API_URL environment variable required", file=sys.stderr)
    sys.exit(1)
API_KEY = os.environ.get("GRAPHIFY_API_KEY", "")
if not API_KEY:
    print("ERROR: GRAPHIFY_API_KEY environment variable required", file=sys.stderr)
    sys.exit(1)
API_MODEL = os.environ.get("GRAPHIFY_API_MODEL", "")
if not API_MODEL:
    print("ERROR: GRAPHIFY_API_MODEL environment variable required", file=sys.stderr)
    sys.exit(1)

RAW_DIR = Path("raw")
OUT_DIR = Path(".graphify-data")
CACHE_DIR = OUT_DIR / "semantic_cache"
GRAPHIFY_OUT_DIR = RAW_DIR / "graphify-out"

BATCH_SIZE = max(1, min(100, int(os.environ.get("GRAPHIFY_BATCH_SIZE", "12"))))
MAX_WORKERS = max(1, min(32, int(os.environ.get("GRAPHIFY_MAX_WORKERS", "8"))))
MAX_RETRIES = max(0, min(10, int(os.environ.get("GRAPHIFY_MAX_RETRIES", "3"))))
RETRY_BASE_DELAY = 4.0
RETRY_MAX_DELAY = 60.0
COMMUNITY_SEED = int(os.environ.get("GRAPHIFY_COMMUNITY_SEED", "42"))
COMMUNITY_RESOLUTION = float(os.environ.get("GRAPHIFY_COMMUNITY_RESOLUTION", "1.0"))
ENABLE_GLEANING = os.environ.get("GRAPHIFY_GLEANING", "true").lower() in ("true", "1", "yes")
GLEANING_MAX_ROUNDS = max(0, min(3, int(os.environ.get("GRAPHIFY_GLEANING_MAX", "1"))))
GLEANING_EXISTING_MAX_CHARS = 3000
GLEANING_DOCUMENTS_MAX_CHARS = 12000
SAFE_NODE_ATTRS = {"label", "type", "source_file"}
SAFE_EDGE_ATTRS = {"relation", "edge_type", "confidence_score"}

CACHE_DIR.mkdir(parents=True, exist_ok=True)

for f in CACHE_DIR.rglob("*.tmp"):
    if f.is_file():
        f.unlink(missing_ok=True)

EXTRACTION_PROMPT = """You are a knowledge graph extraction engine. Read the following documents and extract entities (nodes) and relationships (edges).

Output ONLY valid JSON with this exact schema:
{
  "nodes": [
    {"id": "unique_snake_case", "label": "Human-readable name", "type": "concept|tool|method|framework|project|person|organization", "source_file": "relative/path/from/raw.ext"}
  ],
  "edges": [
    {"source": "node_id", "target": "node_id", "relation": "verb phrase", "edge_type": "EXTRACTED|INFERRED", "confidence_score": 0.9}
  ]
}

Rules:
- EXTRACTED: relationship explicitly stated in source (citation, "uses X", "depends on Y")
- INFERRED: reasonable inference from context
- Extract named concepts, tools, methods, frameworks, projects, people, organizations
- Include rationale edges where documents explain WHY decisions were made
- Do NOT add trivially similar things as semantically_similar_to
- Keep node IDs short, unique, snake_case
- One entity can appear in multiple files — use the SAME id for the same concept
- source_file MUST be the exact relative path shown in the FILE header, not just the basename

Documents:
"""

GLEANING_PROMPT = """You previously extracted entities and relationships from the documents below.
Review your previous extraction and the source documents. Are there any IMPORTANT entities or relationships that were missed?

Focus on:
- Named tools, frameworks, libraries mentioned in passing
- People and organizations referenced indirectly
- Implicit dependencies ("we use X for Y" implies depends_on relationship)
- Concepts that are central to the topic but not the main subject

Output ONLY valid JSON with the same schema, containing ONLY genuinely new items not already in the extraction.
If nothing important was missed, output: {{"nodes": [], "edges": []}}

Previous extraction:
{existing_extraction}

Source documents:
{documents}"""


def source_id(p: Path) -> str:
    """Stable file identifier used in prompts, cache metadata, and node provenance."""
    return p.relative_to(RAW_DIR).as_posix()


def cache_path_for(p: Path) -> Path:
    """Store cache files under semantic_cache/ using the raw/ relative path."""
    rel = p.relative_to(RAW_DIR)
    return CACHE_DIR.joinpath(*rel.parts[:-1], f"{rel.name}.json")


def normalize_source_ref(value) -> str:
    """Normalize model-emitted source references to the canonical source_id format."""
    text = str(value or "").strip().replace("\\", "/")
    while text.startswith("./"):
        text = text[2:]
    if text.startswith("raw/"):
        text = text[4:]
    return text


def is_generated_output(p: Path) -> bool:
    """Skip graphify outputs so the graph does not ingest its own exports."""
    if p.name.startswith(".graphify"):
        return True
    try:
        p.relative_to(GRAPHIFY_OUT_DIR)
        return True
    except ValueError:
        return False


def get_source_files():
    """Get corpus files, excluding generated graphify output."""
    all_files = []
    for ext in ("*.md", "*.txt"):
        for p in RAW_DIR.rglob(ext):
            if not is_generated_output(p):
                all_files.append(p)
    return sorted(all_files)


def list_legacy_cache_files(all_files):
    """Detect old flat cache files left behind by the basename-based cache scheme."""
    current_root_cache_paths = {
        cache_path_for(p).resolve()
        for p in all_files
        if cache_path_for(p).parent == CACHE_DIR
    }
    legacy_files = []
    for cache_file in CACHE_DIR.glob("*.json"):
        if cache_file.is_file() and cache_file.resolve() not in current_root_cache_paths:
            legacy_files.append(cache_file)
    return sorted(legacy_files)


def warn_legacy_cache_files(all_files):
    """Surface legacy cache mismatch instead of silently treating the run as uncached."""
    legacy_files = list_legacy_cache_files(all_files)
    if legacy_files:
        print(
            f"WARNING: Detected {len(legacy_files)} legacy flat cache files in {CACHE_DIR}. "
            "They are ignored by the nested cache layout.",
            flush=True,
        )
        print(
            f"WARNING: Clear {CACHE_DIR} before the first full rebuild to avoid stale cache artifacts.",
            flush=True,
        )


def read_file_content(p, max_chars=6000):
    """Read file content, truncated."""
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
        if len(text) > max_chars:
            text = text[:max_chars] + "\n...[truncated]"
        return text
    except Exception:
        return "[Error reading file]"


def call_api(prompt_content, prompt_prefix=EXTRACTION_PROMPT):
    """Call the API with exponential backoff and full jitter retry."""
    import urllib.error
    import urllib.request

    user_prompt = f"{prompt_prefix}{prompt_content}" if prompt_prefix else prompt_content
    payload = json.dumps({
        "model": API_MODEL,
        "messages": [{"role": "user", "content": user_prompt}],
        "temperature": 0.1,
        "max_tokens": 4096
    }).encode("utf-8")
    req = urllib.request.Request(API_URL, data=payload, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    })
    last_error = None
    for attempt in range(MAX_RETRIES + 1):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                body = resp.read().decode("utf-8")
                data = json.loads(body)
                try:
                    content = data["choices"][0]["message"]["content"]
                except (KeyError, IndexError, TypeError) as e:
                    return json.dumps({"error": f"invalid response schema: {e}"})
                if not isinstance(content, str):
                    return json.dumps({"error": f"non-string API response: {type(content).__name__}"})
                return content
        except json.JSONDecodeError as e:
            last_error = f"JSONDecodeError: {e}"
        except urllib.error.HTTPError as e:
            if e.code in (400, 401, 403, 404, 405, 413, 422):
                body = e.read().decode("utf-8", errors="replace")[:200]
                e.close()
                return json.dumps({"error": f"HTTP {e.code} (no retry): {body}"})
            last_error = f"HTTP {e.code}: {e.reason}"
            e.close()
        except (urllib.error.URLError, TimeoutError, OSError, ConnectionResetError) as e:
            last_error = f"{type(e).__name__}: {e}"

        if attempt < MAX_RETRIES:
            delay = min(RETRY_MAX_DELAY, RETRY_BASE_DELAY * (2 ** attempt))
            jittered = delay * random.random()
            print(
                f"    Retry {attempt + 1}/{MAX_RETRIES} after {jittered:.1f}s (last: {last_error})",
                flush=True,
            )
            time.sleep(jittered)

    return json.dumps({"error": f"Failed after {MAX_RETRIES} retries: {last_error}"})


def parse_extraction(text):
    """Parse extraction result, handling markdown fences."""
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            idx = text.index("{")
            return json.JSONDecoder().raw_decode(text, idx)[0]
        except (json.JSONDecodeError, ValueError):
            pass
        return {"nodes": [], "edges": [], "parse_error": text[:200]}


def dedupe_nodes(nodes):
    """Keep the first occurrence of each node id."""
    seen_ids = set()
    deduped_nodes = []
    for n in nodes:
        nid = n.get("id", "")
        if nid and nid not in seen_ids:
            seen_ids.add(nid)
            deduped_nodes.append(n)
    return deduped_nodes


def edge_identity(edge):
    """Exact edge identity used for extraction-level deduplication."""
    score = edge.get("confidence_score")
    rounded = round(score, 1) if isinstance(score, (int, float)) else score
    return (
        edge.get("source"),
        edge.get("target"),
        edge.get("relation"),
        edge.get("edge_type"),
        rounded,
    )


def dedupe_edges(edges):
    """Keep exact edge records while removing duplicate repeats across cache/new merges."""
    seen_edges = set()
    deduped_edges = []
    for edge in edges:
        identity = edge_identity(edge)
        if identity not in seen_edges:
            seen_edges.add(identity)
            deduped_edges.append(edge)
    return deduped_edges


def merge_extractions(*extractions):
    """Merge cached and freshly extracted data into one exact-deduped extraction."""
    nodes = []
    edges = []
    for extraction in extractions:
        if extraction:
            nodes.extend(extraction.get("nodes", []))
            edges.extend(extraction.get("edges", []))
    return {"nodes": dedupe_nodes(nodes), "edges": dedupe_edges(edges)}


def write_extraction(extraction):
    """Persist the canonical merged extraction used for graph rebuilds."""
    (OUT_DIR / "semantic_extraction.json").write_text(
        json.dumps(extraction, ensure_ascii=False), encoding="utf-8"
    )


def load_cache_entry(cache_file, expected_source):
    """Load one cache entry; malformed entries are treated as missing."""
    try:
        entry = json.loads(cache_file.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"WARNING: Failed to read cache {cache_file}: {e}", flush=True)
        return None

    cached_source = normalize_source_ref(entry.get("source", ""))
    if cached_source and cached_source != expected_source:
        print(
            f"WARNING: Ignoring cache {cache_file} because source '{cached_source}' != '{expected_source}'",
            flush=True,
        )
        return None

    nodes = []
    for node in entry.get("nodes", []):
        if "id" not in node:
            continue
        normalized = dict(node)
        normalized["source_file"] = expected_source
        nodes.append(normalized)

    return {"nodes": nodes, "edges": entry.get("edges", [])}


def load_cached_extraction(all_files):
    """Load the current-format cache and return cached data plus uncached files."""
    cached_nodes = []
    cached_edges = []
    uncached = []
    cached_hits = 0

    for p in all_files:
        cache_file = cache_path_for(p)
        if not cache_file.exists():
            uncached.append(p)
            continue

        entry = load_cache_entry(cache_file, source_id(p))
        if entry is None:
            uncached.append(p)
            continue

        cached_hits += 1
        cached_nodes.extend(entry.get("nodes", []))
        cached_edges.extend(entry.get("edges", []))

    return {"nodes": cached_nodes, "edges": cached_edges}, uncached, cached_hits


def resolve_node_source(raw_source, batch_files):
    """Resolve model-emitted source_file to the canonical relative path for this batch."""
    normalized = normalize_source_ref(raw_source)
    by_source = {source_id(p).lower(): source_id(p) for p in batch_files}
    by_name = {}
    for p in batch_files:
        by_name.setdefault(p.name.lower(), []).append(source_id(p))

    if normalized.lower() in by_source:
        return by_source[normalized.lower()]

    matches = by_name.get(normalized.lower(), [])
    if len(matches) == 1:
        return matches[0]

    if len(batch_files) == 1:
        return source_id(batch_files[0])

    return None


def write_cache_entry(p: Path, nodes, edges):
    """Persist one per-file cache entry using the nested cache layout."""
    source_ref = source_id(p)
    cache_entry = {"nodes": nodes, "edges": edges, "source": source_ref}
    cache_file = cache_path_for(p)
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    tmp_file = cache_file.with_suffix(".tmp")
    tmp_file.write_text(json.dumps(cache_entry, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp_file.replace(cache_file)


def _truncate_text(text, limit, suffix):
    """Keep prompt fragments bounded so gleaning stays cheaper than the first pass."""
    if len(text) > limit:
        return text[:limit] + suffix
    return text


def _run_gleaning(batch_content, current_extraction, batch_num, round_num):
    """Run one gleaning round to recover important misses from the first extraction."""
    existing_json = json.dumps(
        {"nodes": current_extraction.get("nodes", []), "edges": current_extraction.get("edges", [])},
        ensure_ascii=False,
        indent=2,
    )
    existing_json = _truncate_text(existing_json, GLEANING_EXISTING_MAX_CHARS, "\n...[truncated]")
    documents_excerpt = _truncate_text(
        batch_content,
        GLEANING_DOCUMENTS_MAX_CHARS,
        "\n...[truncated for gleaning]",
    )
    gleaning_content = GLEANING_PROMPT.format(
        existing_extraction=existing_json,
        documents=documents_excerpt,
    )

    gleaning_text = call_api(gleaning_content, prompt_prefix="")
    gleaning_result = parse_extraction(gleaning_text)
    if "error" in gleaning_result:
        print(
            f"  WARNING: Gleaning API error in batch {batch_num} round {round_num}: {gleaning_result['error']}",
            flush=True,
        )
        return {"nodes": [], "edges": []}

    new_nodes = len(gleaning_result.get("nodes", []))
    new_edges = len(gleaning_result.get("edges", []))
    if new_nodes > 0 or new_edges > 0:
        print(
            f"  Gleaning round {round_num}: recovered {new_nodes} nodes, {new_edges} edges",
            flush=True,
        )
    else:
        print(f"  Gleaning round {round_num}: no new entities found", flush=True)
    return gleaning_result


def process_batch(batch_files, batch_num, total_batches):
    """Process a batch of files."""
    parts = []
    for p in batch_files:
        content = read_file_content(p)
        parts.append(f"--- FILE: {source_id(p)} ---\n{content}\n")
    batch_content = "\n".join(parts)

    print(f"  Batch {batch_num}/{total_batches}: {len(batch_files)} files, {len(batch_content)} chars", flush=True)
    result_text = call_api(batch_content)
    result = parse_extraction(result_text)

    if "error" in result:
        print(f"  WARNING: API error in batch {batch_num}: {result['error']}", flush=True)
    elif ENABLE_GLEANING and "parse_error" not in result:
        for round_num in range(1, GLEANING_MAX_ROUNDS + 1):
            gleaning_result = _run_gleaning(batch_content, result, batch_num, round_num)
            if not gleaning_result.get("nodes") and not gleaning_result.get("edges"):
                break
            result = merge_extractions(result, gleaning_result)

    grouped_nodes = {source_id(p): [] for p in batch_files}
    unresolved_nodes = 0
    dropped_ids = []
    for node in result.get("nodes", []):
        if "id" not in node:
            continue
        resolved_source = resolve_node_source(node.get("source_file", ""), batch_files)
        if not resolved_source:
            unresolved_nodes += 1
            if len(dropped_ids) < 10:
                dropped_ids.append(node.get("id", "?"))
            continue
        normalized = dict(node)
        normalized["source_file"] = resolved_source
        grouped_nodes[resolved_source].append(normalized)

    if unresolved_nodes:
        print(f"  WARNING: Dropped {unresolved_nodes} unresolved source_file nodes in batch {batch_num}: {dropped_ids}", flush=True)

    nodes = []
    for source_ref in grouped_nodes:
        nodes.extend(grouped_nodes[source_ref])

    valid_node_ids = {node["id"] for node in nodes}
    edges = []
    dropped_edges = 0
    for edge in result.get("edges", []):
        src = edge.get("source")
        tgt = edge.get("target")
        if src in valid_node_ids and tgt in valid_node_ids:
            edges.append(edge)
        else:
            dropped_edges += 1

    if dropped_edges:
        print(f"  WARNING: Dropped {dropped_edges} edges with unresolved endpoints in batch {batch_num}", flush=True)

    for p in batch_files:
        source_ref = source_id(p)
        file_nodes = grouped_nodes[source_ref]
        node_ids = {node["id"] for node in file_nodes}
        file_edges = [
            edge for edge in edges
            if edge.get("source") in node_ids or edge.get("target") in node_ids
        ]
        write_cache_entry(p, file_nodes, file_edges)

    return {"nodes": nodes, "edges": edges, "files": len(batch_files)}


def main():
    all_files = get_source_files()
    warn_legacy_cache_files(all_files)
    cached_extraction, files_to_process, cached_hits = load_cached_extraction(all_files)
    total = len(files_to_process)
    print(
        f"Files total: {len(all_files)} ({cached_hits} cache hits, {total} uncached) "
        f"(batch size: {BATCH_SIZE}, workers: {MAX_WORKERS})"
    )

    if total == 0:
        extraction = merge_extractions(cached_extraction)
        print(f"All files cached. Rebuilding from merged cache ({len(extraction['nodes'])} nodes, {len(extraction['edges'])} edges).")
        write_extraction(extraction)
        return build_graph(extraction)

    batches = []
    for i in range(0, total, BATCH_SIZE):
        batches.append(files_to_process[i:i + BATCH_SIZE])

    total_batches = len(batches)
    print(f"Batches: {total_batches}")

    new_nodes = []
    new_edges = []
    t0 = time.time()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {}
        for i, batch in enumerate(batches, 1):
            future = pool.submit(process_batch, batch, i, total_batches)
            futures[future] = i

        done = 0
        for future in as_completed(futures):
            done += 1
            try:
                result = future.result()
                new_nodes.extend(result["nodes"])
                new_edges.extend(result["edges"])
                elapsed = time.time() - t0
                print(
                    f"  Progress: {done}/{total_batches} batches done ({done*100//total_batches}%) {elapsed:.0f}s",
                    flush=True,
                )
            except Exception as e:
                import traceback
                print(f"  Batch error: {e}\n{traceback.format_exc()}", flush=True)

    elapsed = time.time() - t0
    print(f"\nExtraction complete: {len(new_nodes)} new nodes, {len(new_edges)} new edges in {elapsed:.0f}s")

    extraction = merge_extractions(cached_extraction, {"nodes": new_nodes, "edges": new_edges})
    print(
        f"Merged extraction: {len(extraction['nodes'])} unique nodes, "
        f"{len(extraction['edges'])} exact-deduped edges"
    )
    write_extraction(extraction)
    build_graph(extraction)


def build_graph(extraction=None):
    """Build the report graph and export a link-preserving graph.json."""
    try:
        import networkx as nx
        from networkx.algorithms.community import louvain_communities
    except ImportError:
        print("WARNING: networkx not installed. Skipping graph build.", flush=True)
        return

    if extraction is None:
        extraction_path = OUT_DIR / "semantic_extraction.json"
        if extraction_path.exists():
            extraction = json.loads(extraction_path.read_text(encoding="utf-8"))
        else:
            print("No extraction data found")
            return

    node_records = []
    node_index = {}
    for node in extraction.get("nodes", []):
        node_id = node.get("id")
        if not node_id or node_id in node_index:
            continue
        record = {"id": node_id}
        record.update({key: value for key, value in node.items() if key in SAFE_NODE_ATTRS})
        node_records.append(record)
        node_index[node_id] = record

    valid_links = []
    seen_links = set()
    for edge in extraction.get("edges", []):
        src = edge.get("source")
        tgt = edge.get("target")
        if src not in node_index or tgt not in node_index:
            continue
        record = {"source": src, "target": tgt}
        record.update({key: value for key, value in edge.items() if key in SAFE_EDGE_ATTRS})
        identity = edge_identity(record)
        if identity not in seen_links:
            seen_links.add(identity)
            valid_links.append(record)

    print(f"\nBuilding graph: {len(node_records)} nodes, {len(valid_links)} valid links")

    # Undirected projection for community detection and degree analysis only;
    # graph.json links array preserves full directionality independently.
    projection = nx.Graph()
    for record in node_records:
        projection.add_node(record["id"], **{key: value for key, value in record.items() if key != "id"})
    for edge in valid_links:
        projection.add_edge(edge["source"], edge["target"])

    print(
        f"Projection: {projection.number_of_nodes()} nodes, {projection.number_of_edges()} undirected edges "
        f"from {len(valid_links)} preserved links"
    )

    raw_communities = louvain_communities(
        projection,
        seed=COMMUNITY_SEED,
        resolution=COMMUNITY_RESOLUTION,
    )
    isolated_nodes = {node_id for node_id in projection.nodes() if projection.degree(node_id) == 0}
    communities = []
    for community in raw_communities:
        active = community - isolated_nodes
        if active:
            communities.append(active)
    communities = sorted(communities, key=len, reverse=True)

    for node_id in isolated_nodes:
        if node_id in node_index:
            node_index[node_id]["community"] = -1
    for community_id, community in enumerate(communities):
        for node_id in community:
            if node_id in node_index:
                node_index[node_id]["community"] = community_id
    for record in node_records:
        record.setdefault("community", -1)
    print(f"Communities: {len(communities)} ({len(isolated_nodes)} isolated nodes excluded)")

    data = {
        "directed": True,
        "multigraph": True,
        "graph": {},
        "nodes": node_records,
        "links": valid_links,
    }
    (OUT_DIR / "graph.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    report_lines = [
        "# Knowledge Graph Report\n",
        f"Generated: {time.strftime('%Y-%m-%d %H:%M')}\n",
        (
            f"Nodes: {projection.number_of_nodes()}, Undirected Edges: {projection.number_of_edges()}, "
            f"Preserved Links: {len(valid_links)}, Communities: {len(communities)}\n"
        ),
        "\n## Top Nodes (by degree)\n",
    ]
    for node_id, degree in sorted(projection.degree(), key=lambda item: -item[1])[:30]:
        label = projection.nodes[node_id].get("label", node_id)
        report_lines.append(f"- **{label}** ({node_id}): degree {degree}")

    report_lines.append("\n## Communities\n")
    for i, community in enumerate(sorted(communities, key=len, reverse=True)[:20]):
        community_list = list(community)
        community_set = set(community_list)
        internal_edges = sum(
            1 for u, v in projection.edges(community_list)
            if v in community_set
        )
        n = len(community_list)
        cohesion = (2 * internal_edges / (n * (n - 1))) if n > 1 else 1.0
        top_node = max(community_list, key=lambda nid: projection.degree(nid))
        label = projection.nodes[top_node].get("label", top_node)
        labels = [projection.nodes[nid].get("label", nid) for nid in community_list[:10]]
        report_lines.append(f'### Community {i+1} - "{label}"\n')
        report_lines.append(f"Cohesion: {cohesion:.2f}\n")
        report_lines.append(f"Nodes ({n}): {', '.join(labels)}\n")

    (OUT_DIR / "GRAPH_REPORT.md").write_text("".join(report_lines), encoding="utf-8")

    try:
        from graphify.detect import detect as _detect, save_manifest as _save_manifest

        _detect_result = _detect(RAW_DIR)
        _save_manifest(_detect_result["files"], str(OUT_DIR / "manifest.json"))
    except ImportError:
        print("WARNING: graphify not installed. Skipping manifest generation.", flush=True)

    print(f"\nDone! Graph saved to {OUT_DIR / 'graph.json'}")
    print(f"Report saved to {OUT_DIR / 'GRAPH_REPORT.md'}")

    import shutil

    target_dir = GRAPHIFY_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    for fname in ["graph.json", "GRAPH_REPORT.md", "manifest.json"]:
        src = OUT_DIR / fname
        if src.exists():
            shutil.copy2(src, target_dir / fname)
    print(f"Synced to {target_dir}")


if __name__ == "__main__":
    main()
