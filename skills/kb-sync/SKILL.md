---
name: kb-sync
description: 知识库全量同步（scan + apply + lint + index）
user_invocable: true
---

# 知识库全量同步 (/kb-sync)

一键执行完整的知识库同步管线：scan → apply → lint → index。

依次执行：
```bash
cd <KB_SCRIPTS_PATH>
node kb.js scan
node kb.js apply --draft-mode none
node kb.js lint
node kb.js index
```

向用户展示最终摘要：
- 新增/变更文件数
- frontmatter 修复数
- lint 各项检查结果
- 覆盖率
- 索引更新状态

如果有 scan 发现 0 新文件，直接告知"无需同步，知识库已是最新"。
