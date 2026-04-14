---
name: kb-apply
description: 入库新资料到知识库
user_invocable: true
---

# 知识库入库 (/kb-apply)

将扫描发现的新资料从 `<CLAUDE_DOCS_PATH>` 同步到 `<KNOWLEDGE_BASE_PATH>/raw/`。

执行步骤：
1. 先跑 scan 确认新文件：
```bash
cd <KB_SCRIPTS_PATH> && node kb.js scan
```

2. 展示新文件列表给用户确认

3. 用户确认后执行 apply：
```bash
cd <KB_SCRIPTS_PATH> && node kb.js apply --draft-mode none
```

4. apply 完成后自动跑 lint：
```bash
cd <KB_SCRIPTS_PATH> && node kb.js lint
```

5. 更新索引：
```bash
cd <KB_SCRIPTS_PATH> && node kb.js index
```

向用户展示最终结果：复制了多少文件、frontmatter 修复数、lint 状态。
