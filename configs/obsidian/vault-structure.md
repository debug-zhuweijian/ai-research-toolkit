# Recommended Obsidian Vault Structure

## Directory Layout

```
<YOUR_OBSIDIAN_VAULT>/
├── .obsidian/           # Obsidian config (auto-generated)
├── base/                # Paper notes and document content
│   ├── <AuthorYear_Title>/
│   │   ├── <name>_EN.pdf    # English original
│   │   ├── <name>_ZH.pdf    # Chinese original (if any)
│   │   ├── <name>_EN.md     # English Markdown (converted by MinerU)
│   │   └── <name>_ZH.md     # Chinese Markdown (if any)
│   └── *.md                  # Standalone notes
├── templates/           # Obsidian templates
└── README.md
```

## Naming Convention

Papers and documents should follow this naming pattern:

```
Format: AuthorYear_ShortTitle
Example: Metzger2023_Neuroprosthesis_Speech_Avatar

Forbidden: pure numbers, hashes, garbled characters, filenames with spaces
```

### Naming Priority

1. Academic paper → `FirstAuthorYear_ShortTitle` (extracted from PDF content)
2. Technical doc → `ProjectName_DocType`
3. Unsure → ask the user

## Rules

- `base/` only contains notes and document content
- Plugin configs stay at the vault root level
- Each PDF corresponds to exactly one MD file
- Do NOT save .txt files; use .md only
