# Phase 3: AI 论文分析与学术写作

本阶段将 AI 工具应用于学术研究的核心环节——论文阅读、深度调研和学术写作。通过 Claude Code 的 Skills 和 MCP 服务器组合，你可以快速完成单篇论文精读、多文献横向对比调研、以及高质量学术文稿的起草。

---

## 1. 本阶段工具

| 工具 | 类型 | 用途 |
|------|------|------|
| `/paper-review` | Skill | 单篇论文结构化审阅，输出方法/实验/贡献/局限等报告 |
| `/deep-research-v5` | Skill | 多子代理深度调研，支持横向对比、时间线梳理、综合报告 |
| `/academic-writing` | Skill | 学术论文写作辅助，支持 Introduction/Method/Discussion 等各部分 |
| `/group-meeting-slides` | Skill | 组会演示文稿生成，从论文内容到 PPT 一键完成 |
| `sequential-thinking` MCP | MCP 服务器 | 结构化推理链，支持多步分析和假设验证 |
| `web-search-prime` MCP | MCP 服务器 | 网络搜索，获取最新文献和资料 |
| `web-reader` MCP | MCP 服务器 | 网页内容抓取与 Markdown 转换 |
| `zai-mcp-server` MCP | MCP 服务器 | 图像/视频分析，支持图表解读、截图 OCR 等 |
| `MinerU` MCP | MCP 服务器 | PDF/PPT/Word 转 Markdown，学术论文格式转换 |

---

## 2. 安装步骤

### 2.1 Skills 安装

本阶段涉及的 Skills 已通过 Phase 1 全局安装，无需额外操作。确认以下 Skill 可用：

```bash
# 在 Claude Code 中验证
/paper-review --help
/deep-research-v5 --help
/academic-writing --help
/group-meeting-slides --help
```

如果提示找不到，请回到 Phase 1 重新安装对应的 Skill 包。

### 2.2 MCP 服务器配置

确保以下 MCP 服务器已在 `~/.claude.json`（或项目级 `.claude.json`）中配置：

```jsonc
{
  "mcpServers": {
    // 结构化推理（npm 全局安装）
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-sequential-thinking"],
      "type": "stdio"
    },

    // 网络搜索（需要智谱 BigModel API Key）
    "web-search-prime": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-web-search-prime"],
      "env": {
        "BIGMODEL_API_KEY": "your_zhipu_api_key_here"
      },
      "type": "stdio"
    },

    // 网页抓取（需要智谱 BigModel API Key）
    "web-reader": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-web-reader"],
      "env": {
        "BIGMODEL_API_KEY": "your_zhipu_api_key_here"
      },
      "type": "stdio"
    },

    // 图像/视频分析
    "zai-mcp-server": {
      "command": "npx",
      "args": ["-y", "@anthropic/zai-mcp-server"],
      "type": "stdio"
    }
  }
}
```

> **提示**：`web-search-prime`、`web-reader` 共用同一个智谱 BigModel API Key，在 [open.bigmodel.cn](https://open.bigmodel.cn) 注册即可获取免费额度。详见 [API Keys Guide](./api-keys-guide.md)。

### 2.3 验证 MCP 连接

在 Claude Code 中执行以下测试：

```
请用 web-search-prime 搜索 "neural speech decoding 2025"
```

如果返回搜索结果，说明 MCP 服务器配置正确。

---

## 3. 使用示例

### 3.1 单篇论文审阅

**场景**：读一篇 PDF 论文，获取结构化审阅报告。

**前置步骤**：先用 MinerU 将 PDF 转为 Markdown：

```
请用 MinerU 的 parse_documents 将论文 PDF 转为 Markdown
文件路径：G:\obsidian\base\Smith2024_Neural_Decoding\Smith2024_Neural_Decoding.pdf
```

**执行审阅**：

```
/paper-review Smith2024_Neural_Decoding.md
```

**输出报告结构**：

```
## 论文审阅报告

### 基本信息
- 标题：...
- 作者：...
- 发表期刊/会议：...
- 年份：...

### 研究问题与动机
...

### 方法 (Method)
- 核心方法：...
- 创新点：...
- 与已有方法的区别：...

### 实验设计 (Experimental Design)
- 数据集：...
- 评估指标：...
- 基线方法：...
- 消融实验：...

### 证据质量 (Evidence Quality)
- 统计显著性：...
- 效果量：...
- 可复现性评估：...

### 主要贡献 (Contributions)
1. ...
2. ...
3. ...

### 局限性 (Limitations)
1. ...
2. ...
3. ...

### 关键要点 (Key Takeaways)
- 对本领域的影响：...
- 可借鉴之处：...
- 未来方向：...
```

### 3.2 深度调研

**场景**：对某个研究方向进行多文献横向对比。

```
/deep-research-v5 "对比 2020-2025 年间基于深度学习的语音解码方法，
包括 EEG、ECoG、声学特征提取等技术路线的优缺点"
```

**输出**：
- 多子代理并行搜索和阅读文献
- 自动汇总对比表格
- 附引用来源的调研报告
- 时间线演进梳理

> 详见下方第 4 节的详细说明。

### 3.3 学术写作

**场景**：撰写论文的某个章节。

```
/academic-writing "撰写关于神经语音解码领域的 Introduction，
重点从 Broca/Wernicke 的经典发现过渡到现代深度学习方法，
引用 10-15 篇关键文献"
```

**支持的场景**：
- 撰写 Introduction（研究背景与动机）
- 撰写 Related Work（相关工作综述）
- 撰写 Method（方法描述）
- 撰写 Discussion（讨论与展望）
- 修改润色已有文稿
- 调整学术英语表达

### 3.4 组会 PPT

**场景**：准备组会论文汇报。

```
/group-meeting-slides
```

该 Skill 会引导你提供论文内容，自动生成学术风格的演示文稿。支持：
- 论文背景页
- 方法架构图（Mermaid 或 Draw.io）
- 实验结果页
- 讨论与总结页

---

## 4. deep-research-v5 详细说明

### 4.1 工作原理

`/deep-research-v5` 是一个多代理（multi-agent）调研系统，采用"Lead Agent + Subagents"架构：

```
┌─────────────────────────────────────────┐
│              Lead Agent                  │
│  · 解析研究问题                          │
│  · 制定搜索策略                          │
│  · 分配子任务                            │
│  · 汇总最终报告                          │
└──────────┬──────────┬───────────────────┘
           │          │
     ┌─────▼───┐ ┌───▼──────┐ ┌──────────┐
     │Subagent │ │Subagent  │ │Subagent  │
     │ 文献搜索 │ │ 数据分析  │ │ 对比总结  │
     └─────┬───┘ └───┬──────┘ └────┬─────┘
           │         │             │
     ┌─────▼─────────▼─────────────▼─────┐
     │          MCP 工具层                 │
     │  web-search-prime / web-reader /   │
     │  sequential-thinking / zai         │
     └───────────────────────────────────┘
```

**执行流程**：

1. **问题解析**：Lead Agent 分析你的研究问题，拆解为多个子问题
2. **搜索策略**：为每个子问题制定关键词和搜索路径
3. **并行调研**：多个 Subagent 同时执行搜索和阅读
4. **信息整合**：Lead Agent 汇总各子代理的结果
5. **报告生成**：输出结构化调研报告，附完整引用

### 4.2 使用的 MCP 工具

| MCP 工具 | 用途 |
|----------|------|
| `web-search-prime` | 搜索学术文献、技术博客、数据集 |
| `web-reader` | 抓取论文全文、技术文档 |
| `sequential-thinking` | 多步推理、假设验证、逻辑链构建 |
| `zai-mcp-server` | 分析论文中的图表、架构图 |

### 4.3 输出格式

```
# 深度调研报告：[研究主题]

## 执行摘要
[2-3 段概述核心发现]

## 1. 背景与动机
[问题背景、研究意义]

## 2. 方法对比
| 方法 | 年份 | 数据模态 | 关键技术 | 最佳性能 | 局限性 |
|------|------|----------|----------|----------|--------|
| ... | ... | ... | ... | ... | ... |

## 3. 技术演进时间线
[按时间梳理关键突破]

## 4. 当前挑战与机遇
[未解决的问题、新兴方向]

## 5. 结论与建议
[总结性建议]

## 参考文献
[1] Author et al., "Title", Journal/Conference, Year.
...
```

### 4.4 使用技巧

1. **精确的查询**：给出具体的时间范围、技术关键词、对比维度
2. **逐步深入**：先做宽泛调研，再对感兴趣的方向做二次 deep-research
3. **结合 paper-review**：对调研中发现的关键论文，用 `/paper-review` 做精读
4. **保存结果**：调研报告建议保存到 `G:\obsidian\base\<主题名>\` 目录

---

## 5. 与下一阶段衔接

Phase 3 产出的论文笔记、调研报告、写作草稿是 Phase 4 知识库的核心素材：

| Phase 3 产出 | Phase 4 归档位置 |
|---------------|------------------|
| 论文审阅报告 | `G:\obsidian\base\<论文名>\*_review.md` |
| 深度调研报告 | `G:\obsidian\base\<主题名>\research_report.md` |
| 学术写作草稿 | `G:\obsidian\base\<项目名>\draft\` |
| 组会 PPT | `I:\claude-docs\ppt\` |

建议在每个 Phase 3 任务完成后，立即将产出同步到知识库（Phase 4 的 `/kb-scan` 会自动处理）。

---

## 6. 常见问题

### Q1: /paper-review 对非英文论文支持如何？

完全支持中文论文。MinerU 的 OCR 可以处理中文 PDF，`/paper-review` 的审阅报告也会跟随论文语言。如果需要中文审阅英文论文，可以在命令后加上"请用中文输出报告"。

### Q2: deep-research-v5 运行时间很长怎么办？

深度调研涉及多轮搜索和阅读，通常需要 3-10 分钟。如果时间过长：
- 缩小研究范围（更具体的关键词）
- 减少时间跨度（如"2023-2025"而非"2020-2025"）
- 确认网络连接正常（MCP 服务器需要联网）

### Q3: 学术写作的引用格式可以自定义吗？

可以。在 `/academic-writing` 的提示中指定格式要求，例如：
```
/academic-writing "撰写 Related Work，使用 IEEE 引用格式"
```
支持 APA、IEEE、ACM、MLA 等常见格式。注意 AI 生成的引用可能存在虚构（hallucination），务必人工核实每条引用。

### Q4: 组会 PPT 可以导出为 .pptx 吗？

`/group-meeting-slides` 支持 `.pptx` 和 `.pdf` 两种输出格式。如需使用 `academic-pptx` skill 获得更学术化的模板：
```
/academic-pptix "生成关于 XXX 论文的组会汇报 PPT"
```

### Q5: web-search-prime 搜索不到最新的论文怎么办？

`web-search-prime` 依赖网页搜索而非学术数据库。对于最新论文：
1. 尝试使用 `search_recency_filter: "oneMonth"` 限制时间范围
2. 对 arXiv 等平台，用 `web-reader` 直接抓取论文页面
3. 结合 `/paper-search` skill 搜索学术数据库

---

## 7. Windows 注意事项

1. **路径格式**：在 Claude Code 中使用 Git Bash 路径格式（如 `/g/obsidian/base/` 而非 `G:\obsidian\base\`），但 MCP 工具接受 Windows 原生路径
2. **长路径问题**：Windows 默认路径长度限制为 260 字符，建议论文文件夹名控制在 50 字符以内
3. **编码**：确保 PDF 转 Markdown 时使用 UTF-8 编码，MinerU MCP 默认输出 UTF-8
4. **网络代理**：如果使用 Clash Verge 等代理工具，确保 MCP 服务器的 HTTP/HTTPS 请求走代理通道（通常设置 `HTTP_PROXY` 和 `HTTPS_PROXY` 环境变量即可）
5. **内存占用**：`deep-research-v5` 会启动多个子代理，建议系统可用内存不低于 8GB
6. **文件保存**：所有生成的文件按 CLAUDE.md 中的路由规则保存，PDF 转 MD 结果存到 `G:\obsidian\base\<文档名>\`，PPT 存到 `I:\claude-docs\ppt\`
