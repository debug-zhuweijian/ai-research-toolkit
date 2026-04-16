---
name: kb
description: 知识库维护 — 扫描新资料、入库、健康检查、统计查询
user_invocable: true
---

# 知识库维护 (/kb)

知识库根目录 `I:\knowledge\`，脚本在 `I:\claude-docs\scripts\knowledge-base\kb.js`。

根据用户参数 `$ARGUMENTS` 选择操作：

## 操作列表

| 参数 | 操作 | 命令 |
|------|------|------|
| `scan` | 扫描 claude-docs 有无新资料 | `node kb.js scan` |
| `apply` | 入库新资料（draft-mode none） | `node kb.js apply --draft-mode none` |
| `lint` | 8 项健康检查 | `node kb.js lint` |
| `index` | 重新生成 wiki/index.md | `node kb.js index` |
| `stats` | 打印当前统计 | `node kb.js stats` |
| `sync` | 全量同步（scan → apply → lint → index） | 依次执行上述 4 步 |
| `status` | 状态总览（stats + lint 摘要） | `node kb.js stats` + `node kb.js lint` |

所有命令在 `I:\claude-docs\scripts\knowledge-base\` 目录下执行。

## 执行规则

1. 如果用户只说 `/kb` 不带参数，默认执行 `sync`（全量同步）
2. 如果用户说 `/kb apply`，先跑 scan 看有多少新文件，展示给用户确认后再 apply
3. apply 完成后自动跑 lint，如果 lint 有问题展示报告
4. 最后跑 index 更新索引
5. 展示最终结果摘要（新增文件数、lint 状态、覆盖率）

## 日常使用

- "新资料入库" → `/kb sync`
- "检查有没有新文件" → `/kb scan`
- "看知识库状态" → `/kb stats`
- "跑健康检查" → `/kb lint`
