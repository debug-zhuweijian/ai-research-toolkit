# Version Control & Iteration Tracking Design

## Summary

为 ai-research-toolkit 引入 SemVer 版本号管理，使用 git-cliff 从 conventional commits 自动生成 CHANGELOG.md，配合 git tag 和 GitHub Actions 自动发布 Release。

## Context

- 公开仓库：`debug-zhuweijian/ai-research-toolkit`
- 20 个 commits，0 个 tags，无 CHANGELOG
- 已使用 conventional commits（feat/fix/docs/refactor/chore）
- 纯文档/skill 仓库，无 package.json

## Decisions

### 1. 版本粒度：项目统一版本号

所有 skills、agents、docs 共享一个 SemVer 版本号。理由：
- 项目规模小（20 commits），模块耦合度高
- 单版本号让用户和 GitHub Release 页面一目了然
- 独立 skill 版本号留待项目成熟后再拆分

### 2. 起始版本：v0.1.0

标记在 `59a8966` (initial release commit) 上。所有历史 commits 归入此版本。

### 3. 工具：git-cliff

**安装**：从 GitHub Releases 下载预编译 Windows 二进制。

```bash
# 下载最新版到 ~/bin/
curl -sL https://github.com/orhun/git-cliff/releases/latest/download/git-cliff-x86_64-pc-windows-msvc.zip -o git-cliff.zip
unzip git-cliff.zip -d ~/bin/
```

**选择理由**：
- Rust 单二进制，无运行时依赖
- 高度可配置（cliff.toml）
- 比 standard-version 更适合非 Node 项目

### 4. cliff.toml 配置

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

### 5. 版本号策略

- **Major (x.0.0)**：不兼容的架构变更
- **Minor (0.x.0)**：新 skill/agent/功能（feat commits）
- **Patch (0.0.x)**：Bug 修复、文档更新（fix/docs commits）
- **Tag 格式**：`v{major}.{minor}.{patch}`

### 6. 日常工作流

```
日常开发 (conventional commits)
    ↓
准备发版 → git cliff -o CHANGELOG.md
    ↓
git add CHANGELOG.md && git commit -m "chore: update CHANGELOG for vX.Y.Z"
    ↓
git tag vX.Y.Z && git push --follow-tags
    ↓
GitHub Actions 自动创建 Release
```

### 7. GitHub Actions Release 工作流

`.github/workflows/release.yml`：

```yaml
name: Release
on:
  push:
    tags: ['v*']
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: orhun/git-cliff-action@v4
        with:
          config: cliff.toml
          args: --current
        env:
          OUTPUT: CHANGELOG.md
      - uses: softprops/action-gh-release@v2
        with:
          body_path: CHANGELOG.md
```

### 8. README Release Badge

在两个 README 的 badge 行最前面添加动态版本徽章：

```markdown
[![GitHub Release](https://img.shields.io/github/v/release/debug-zhuweijian/ai-research-toolkit?label=release)](https://github.com/debug-zhuweijian/ai-research-toolkit/releases)
```

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `cliff.toml` | Create | git-cliff 配置 |
| `CHANGELOG.md` | Create | git cliff 自动生成 |
| `.github/workflows/release.yml` | Create | GitHub Actions 自动发布 |
| `README.md` | Edit | 添加 Release badge |
| `README.zh-CN.md` | Edit | 添加 Release badge |

## Out of Scope

- 自动 bump version（手动打 tag 更可控）
- npm/PyPI publish（纯文档仓库无需发包）
- 每个 skill 独立版本号（当前规模不需要）
- pre-release / nightly builds
