---
name: kb-lint
description: 知识库 8 项健康检查
user_invocable: true
---

# 知识库健康检查 (/kb-lint)

对知识库执行 8 项 Lint 检查。

执行：
```bash
cd <KB_SCRIPTS_PATH> && node kb.js lint
```

向用户展示检查结果表格：

| 检查项 | 严重度 | 问题数 |
|--------|--------|--------|
| contradictions | 高 | ? |
| completeness | 中 | ? |
| islands | 低 | ? |
| stale | 中 | ? |
| broken_links | 高 | ? |
| missing_frontmatter | 中 | ? |
| source_coverage | 中 | ? |
| provenance | 低 | ? |

如果有高严重度问题，列出具体内容并建议修复方案。
