---
name: kb-scan
description: 扫描 claude-docs 检查知识库新资料
user_invocable: true
---

# 知识库扫描 (/kb-scan)

扫描 `<CLAUDE_DOCS_PATH>` 检查是否有新文件需要入库到知识库。

执行：
```bash
cd <KB_SCRIPTS_PATH> && node kb.js scan
```

读取输出报告，向用户展示：
- new 文件数及列表
- changed 文件数
- duplicate 文件数

如果有新文件，建议用户运行 `/kb-apply` 入库。
