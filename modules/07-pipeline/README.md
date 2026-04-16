---
phase: 07-pipeline
title: 管道编排
status: planned
---

# Phase 07: 管道编排

跨阶段研究工作流的自动化编排与状态管理。

## 状态：计划中

本模块将在 v0.2.0 发布阶段开发。

## 计划组件

### Skills（计划）

| Skill | 说明 | 状态 |
|-------|------|------|
| `research-pipeline` | 研究工作流状态机（Phase 01-06 编排） | planned |

## 设计目标

```
research-pipeline 设计思路：

  01-discovery --> 02-processing --> 03-analysis
                                         |
                                         v
  06-presentation <-- 05-knowledge <-- 04-writing
```

- 自动检测当前研究阶段
- 管理跨阶段的数据传递
- 支持断点续跑与状态恢复
- 与各模块 skill/agent 无缝集成

## 依赖

- Phase 01-06 所有模块的基础设施
- 工作流状态持久化机制（待设计）
- 跨 MCP server 的协调协议

## 路线图

| 里程碑 | 内容 | 预计版本 |
|--------|------|---------|
| M1 | 基础状态机 + Phase 串联 | v0.2.0-alpha |
| M2 | 断点续跑 + 错误恢复 | v0.2.0-beta |
| M3 | 可视化进度 + 配置化流程 | v0.2.0 |
