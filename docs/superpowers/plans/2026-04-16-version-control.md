# Version Control Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 ai-research-toolkit 引入 SemVer 版本管理、自动 CHANGELOG 生成和 GitHub Release 工作流。

**Architecture:** git-cliff 从 conventional commits 自动生成 CHANGELOG.md，git tag 标记版本，GitHub Actions 在 push tag 时自动创建 Release。README 添加动态版本徽章。

**Tech Stack:** git-cliff (Rust 二进制), GitHub Actions, shields.io

---

### Task 1: 安装 git-cliff

**Files:** (无项目文件变更，仅本地工具安装)

- [ ] **Step 1: 下载 git-cliff Windows 二进制**

```bash
mkdir -p ~/bin
cd /tmp
curl -sL https://github.com/orhun/git-cliff/releases/latest/download/git-cliff-x86_64-pc-windows-msvc.zip -o git-cliff.zip
unzip -o git-cliff.zip -d ~/bin/
```

- [ ] **Step 2: 验证安装**

Run: `git-cliff --version`
Expected: `git-cliff 2.x.x`（显示版本号即成功）

- [ ] **Step 3: 确认 PATH 可达**

Run: `which git-cliff`
Expected: `/c/Users/Windows11/bin/git-cliff.exe` 或类似路径

---

### Task 2: 创建 cliff.toml 配置

**Files:**
- Create: `cliff.toml`

- [ ] **Step 1: 创建 cliff.toml**

在项目根目录 `I:/claude-docs/my-project/ai-research-toolkit/cliff.toml` 创建：

```toml
[changelog]
header = """# Changelog\n\nAll notable changes to this project will be documented in this file.\n"""
trim = true

[git]
conventional_commits = true
filter_unconventional = true
split_commits = false

commit_parsers = [
  { message = "^feat", group = "<!-- 0 -->🚀 Features" },
  { message = "^fix", group = "<!-- 1 -->🐛 Bug Fixes" },
  { message = "^refactor", group = "<!-- 2 -->♻️ Refactor" },
  { message = "^docs", group = "<!-- 3 -->📚 Documentation" },
  { message = "^perf", group = "<!-- 4 -->⚡ Performance" },
  { message = "^ci", group = "<!-- 5 -->👷 CI/CD" },
  { message = "^chore", group = "<!-- 6 -->🔧 Miscellaneous" },
]

protect_breaking_commits = false
filter_commits = true
```

- [ ] **Step 2: 预览 CHANGELOG 确认配置正确**

Run: `cd /i/claude-docs/my-project/ai-research-toolkit && git cliff`
Expected: 输出按 feat/fix/docs 分组的 changelog 内容，无报错

- [ ] **Step 3: Commit**

```bash
cd /i/claude-docs/my-project/ai-research-toolkit
git add cliff.toml
git commit -m "chore: add git-cliff configuration for CHANGELOG generation"
```

---

### Task 3: 生成初始 CHANGELOG.md

**Files:**
- Create: `CHANGELOG.md`

- [ ] **Step 1: 生成 CHANGELOG.md**

Run: `cd /i/claude-docs/my-project/ai-research-toolkit && git cliff -o CHANGELOG.md`
Expected: 生成 CHANGELOG.md，包含所有历史 commits 按 conventional 类型分组

- [ ] **Step 2: 检查生成内容**

Run: `head -30 /i/claude-docs/my-project/ai-research-toolkit/CHANGELOG.md`
Expected: 标题 "# Changelog"，然后是分组后的 commit 列表

- [ ] **Step 3: Commit**

```bash
cd /i/claude-docs/my-project/ai-research-toolkit
git add CHANGELOG.md
git commit -m "chore: generate initial CHANGELOG.md with git-cliff"
```

---

### Task 4: 创建 GitHub Actions Release 工作流

**Files:**
- Create: `.github/workflows/release.yml`

- [ ] **Step 1: 创建 workflow 文件**

在 `I:/claude-docs/my-project/ai-research-toolkit/.github/workflows/release.yml` 创建：

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

permissions:
  contents: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Generate Release Notes
        uses: orhun/git-cliff-action@v4
        with:
          config: cliff.toml
          args: --current
        env:
          OUTPUT: CHANGELOG.md

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          body_path: CHANGELOG.md
```

- [ ] **Step 2: 验证 YAML 语法**

Run: `python3 -c "import yaml; yaml.safe_load(open('/i/claude-docs/my-project/ai-research-toolkit/.github/workflows/release.yml'))"`
Expected: 无报错（Python yaml 解析通过）

- [ ] **Step 3: Commit**

```bash
cd /i/claude-docs/my-project/ai-research-toolkit
git add .github/workflows/release.yml
git commit -m "ci: add GitHub Actions release workflow with git-cliff"
```

---

### Task 5: README 添加 Release Badge

**Files:**
- Modify: `README.md:7` (badge 行)
- Modify: `README.zh-CN.md:7` (badge 行)

- [ ] **Step 1: 修改 README.md**

将第 7 行的 badge 行（以 `[![License` 开头）前面插入 Release badge：

原行：
```
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Ask DeepWiki]...
```

改为：
```
[![GitHub Release](https://img.shields.io/github/v/release/debug-zhuweijian/ai-research-toolkit?label=release)](https://github.com/debug-zhuweijian/ai-research-toolkit/releases) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Ask DeepWiki]...
```

- [ ] **Step 2: 修改 README.zh-CN.md**

同样在第 7 行 badge 行前面插入相同的 Release badge。

- [ ] **Step 3: 验证两个 README 的 badge 行**

Run: `cd /i/claude-docs/my-project/ai-research-toolkit && grep -n "GitHub Release" README.md README.zh-CN.md`
Expected: 两个文件各匹配到一行

- [ ] **Step 4: Commit**

```bash
cd /i/claude-docs/my-project/ai-research-toolkit
git add README.md README.zh-CN.md
git commit -m "docs: add release version badge to bilingual READMEs"
```

---

### Task 6: 打初始 tag 并推送

**Files:** (无文件变更，git tag 操作)

- [ ] **Step 1: 在 initial release commit 上打 tag**

```bash
cd /i/claude-docs/my-project/ai-research-toolkit
git tag v0.1.0 59a8966bb07b36743f802cc1dfed388f4bd53456
```

- [ ] **Step 2: 验证 tag**

Run: `cd /i/claude-docs/my-project/ai-research-toolkit && git tag -l`
Expected: `v0.1.0`

- [ ] **Step 3: 推送所有变更和 tag**

```bash
cd /i/claude-docs/my-project/ai-research-toolkit
git push origin main
git push origin v0.1.0
```

- [ ] **Step 4: 验证 GitHub Actions Release 创建成功**

Run: `gh release view v0.1.0 --repo debug-zhuweijian/ai-research-toolkit`
Expected: 显示 Release 信息和 CHANGELOG 内容

---

## Self-Review Checklist

- [x] **Spec coverage:** 所有 8 个 design decisions 均有对应 task
- [x] **Placeholder scan:** 无 TBD/TODO/"implement later"/"add validation"
- [x] **Type consistency:** 无代码函数调用，配置文件内容完整一致
- [x] **YAGNI:** 无自动 bump、无 npm publish、无 pre-release
