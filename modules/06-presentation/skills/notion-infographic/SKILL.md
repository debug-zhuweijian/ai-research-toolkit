---
name: notion-infographic
description: Notion 风格信息图（Infographic）创建工具
compatibility: >
  Requires web_search and web_fetch. Optimal with subagent dispatch
  (Claude Code, Cowork). Degrades gracefully to single-thread on Claude.ai.
  Image generation requires imageGen tool or manual use of prompts.
---
# Notion Infographic Generator — Agent Pipeline V1

用户给大纲，Agent 去研究，你只管 Plan 和验收。

## Architecture

```
User Outline / Topic
       ↓
Lead Agent (你 — 永远不搜索)
  |
  P0: 环境检测 + 输入解析
  P1: 研究任务板 (拆解大纲为研究任务)
  |
  Dispatch ──→ Expert A ──→ writes task-a.md ──┐
           ──→ Expert B ──→ writes task-b.md ──┤ (parallel)
           ──→ Expert C ──→ writes task-c.md ──┘
  |                                             |
  |     workspace/research-notes/  <────────────┘
  |
  P2: Read notes → 提炼核心观点
  P3: 规划组图结构 (张数 + 每张内容)
  P4: 生成完整提示词 (风格前缀 + 内容 + 风格后缀)
  P5: 验收 + 输出
```

## P0: 环境检测 + 输入解析

```
1. 检测子 Agent 能力:
   - Claude Code / Cowork: YES → 并行派遣
   - Claude.ai: NO → 降级模式 (Lead 自己串行执行研究)
2. web_search / web_fetch 是否可用?
3. imageGen 是否可用? (不可用则输出提示词文本)
4. 解析用户输入:
   - 纯主题/关键词 → 需要全面研究
   - 大纲/要点列表 → 按要点研究
   - 完整文稿 → 提炼观点后补充研究
   - 用户指定张数? → 记录，优先级最高
```

## P1: 研究任务板

Lead Agent 将用户大纲拆解为 3-6 个研究任务。每个任务分配一个专家角色。

**Read `reference/subagent-prompt.md` for the prompt template.**

### 任务板格式

```
# Research Task Board
Topic: {用户主题}
Outline Points: {大纲要点列表}

## Group A (parallel — 核心观点研究)
Task A: [行业分析师] — 研究 {观点1} 的数据支撑和案例
Task B: [技术专家] — 研究 {观点2} 的技术细节和趋势
Task C: [用户研究员] — 研究 {观点3} 的用户痛点和故事

## Group B (parallel — 补充素材)
Task D: [数据挖掘师] — 搜集相关统计数据和图表素材
Task E: [案例猎手] — 搜集经典案例和金句
```

### 任务分配原则

- 每个大纲要点至少分配 1 个研究任务
- 优先研究"需要数据/案例支撑"的观点
- 纯观点类（不需要外部信息）的可以跳过研究
- 总任务数控制在 3-6 个，避免过度发散

### 环境适配派遣

**Claude Code / Cowork (有子Agent):**
```bash
# Parallel dispatch
for task in a b c; do
  claude -p "$(cat workspace/prompts/task-${task}.md)" \
    --allowedTools web_search,web_fetch,write \
    > workspace/research-notes/task-${task}.md &
done
wait
```

**Claude.ai (降级 — 无子Agent):**
Lead Agent 自己串行执行每个任务:
1. 按任务板顺序，依次执行 web_search + web_fetch
2. 每完成一个任务，将发现写入笔记块
3. 完成所有研究后进入 P2

## P2: 提炼核心观点

Lead Agent 阅读所有研究笔记，执行:

1. **信息聚合** — 把分散的发现按大纲要点归类
2. **观点提炼** — 每个要点提炼 1 个可视化核心观点
3. **数据筛选** — 为每个观点挑选最有冲击力的数据/案例
4. **可视化评估** — 判断每个观点是否适合独立成图

### 观点提炼规则

- 每张图只承载 1 个核心观点
- 观点不足时不强行凑数
- 观点过多时合并相近内容
- 硬上限：不超过 12 张

## P3: 规划组图结构

**Read `reference/style-guide.md` for Notion style specifications.**

### 图片数量决策

优先级：用户指定 > 观点分析 > 字数参考

| 内容长度 | 通常观点数 | 参考张数 |
|---------|-----------|---------|
| 短内容 (<500字) | 2-4 | 3-5 张 |
| 中等 (500-1500字) | 4-7 | 5-8 张 |
| 长内容 (>1500字) | 6-10 | 8-12 张 |

### 组图结构

```
第 1 张: 标题封面图 — 主题 + 核心价值主张
第 2~N-1 张: 内容图 — 每张一个核心观点 + 研究数据支撑
第 N 张: 总结/行动号召图
```

每张图的内容规划需包含:
- 核心观点（一句话）
- 视觉化描述（场景、人物动作、图标）
- 关键数据/金句（从研究笔记中提取）
- 中文标注文字（精简版）

## P4: 生成完整提示词

**Read `reference/style-guide.md` for the complete prompt template.**

每张图的提示词 = 风格前缀 + 内容描述 + 风格后缀

内容描述是唯一的变量区域，需要:
- 描述画面场景（简洁、视觉化）
- 融入研究数据（转化为图表/数字元素）
- 指定中文标注文字
- 保持大量留白和呼吸感

### 内容描述写作原则

好的内容描述:
```
一个人站在分岔路口，左边路牌写"传统开发"右边写"AI编程"。
左边路上堆满代码文件，右边是一个机器人助手在帮忙搬运。
底部数据标注：72%开发者已使用AI辅助编码（2025 Stack Overflow）
```

差的内容描述:
```
画一张关于AI编程的图
```

## P5: 验收 + 输出

### 输出格式

为每张图生成完整提示词，保存为 markdown 文件：

```markdown
# Notion Infographic Prompts — {主题}

## 图 1/N: {标题}
**核心观点:** {一句话}
**Prompt:**
{完整提示词 = 风格前缀 + 内容描述 + 风格后缀}

## 图 2/N: {标题}
...
```

### 如果有 imageGen 工具

直接为每张图调用 imageGen，使用生成的提示词。
比例设定 16:9。

### 验收清单

- [ ] 每张图的风格前缀和后缀完整无缺
- [ ] 内容描述融入了研究数据（不是空泛描述）
- [ ] 中文标注文字精简（每张不超过 30 字标注）
- [ ] 组图逻辑连贯（封面→内容→总结）
- [ ] 总张数在合理范围内

## Anti-Hallucination Rules

1. Lead Agent 不编造数据 — 所有数据必须来自研究笔记
2. 研究笔记中没有的数据标注 [待验证]
3. 子 Agent 只使用搜索结果中的真实信息
4. 金句/引用必须标注来源
5. 统计数据必须标注年份和机构

## Progress Reporting

```
[P0 complete] 环境: {claude.ai/code}. 输入类型: {大纲/文稿/关键词}.
[P1 complete] 任务板: {N} 个研究任务, {M} 组并行. 派遣中...
[P1 task-a complete] {N} 条发现, {M} 个数据点.
[P1 all complete] 研究完成. {总发现数} 条发现, {总源数} 个来源.
[P2 complete] 提炼 {N} 个核心观点. 准备规划组图.
[P3 complete] 规划 {N} 张图: 1 封面 + {N-2} 内容 + 1 总结.
[P4 complete] {N} 张提示词生成完毕.
[P5 complete] 验收通过. 输出 {N} 张信息图提示词.
```
