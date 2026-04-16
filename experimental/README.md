# Experimental Components

此目录包含实验性组件，**不推荐普通用户安装**。

## DeepScientist Agents (14)

`deepscientist/` 目录下的 14 个 agent 需要 [DeepScientist](https://github.com/DoriRoth/DeepScientist) 平台才能运行。

### 要求

- DeepScientist 平台安装和配置
- 特定 API 密钥（OpenAI/Anthropic compatible endpoint）
- 标准 Claude Code 环境不包含这些依赖

### Agent 列表

| Agent | 用途 |
|-------|------|
| deepscientist-analysis-campaign | 分析活动管理 |
| deepscientist-baseline | 基线实验 |
| deepscientist-decision | 决策支持 |
| deepscientist-experiment | 实验执行 |
| deepscientist-figure-polish | 图表润色 |
| deepscientist-finalize | 最终定稿 |
| deepscientist-idea | 想法生成 |
| deepscientist-intake-audit | 入口审计 |
| deepscientist-mentor | 指导建议 |
| deepscientist-optimize | 优化迭代 |
| deepscientist-rebuttal | Rebuttal 辅助 |
| deepscientist-review | 审阅模拟 |
| deepscientist-scout | 文献侦察 |
| deepscientist-write | 写作辅助 |

## deep-research（旧版）

`deep-research.md` 是旧版深度研究 agent，已被 `deep-research-v5` 替代。保留供参考。

## 安装

```bash
# 仅在你有 DeepScientist 平台时
cp -r experimental/deepscientist/agents/* ~/.claude/agents/
```
