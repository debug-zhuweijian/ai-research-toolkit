# API Keys 配置指南

本工具包涉及三个 API Key，分别用于 Claude Code 核心、智谱 AI 服务和 MinerU 云端转换。本文档提供每个 Key 的注册、配置和验证的完整步骤。

---

## 快速总览

| API Key | 用途 | 注册地址 | 免费额度 | 必要性 |
|---------|------|----------|----------|--------|
| Anthropic API Key（或兼容端点 Key） | Claude Code 核心 | console.anthropic.com 或兼容端点 | Anthropic: $5 最低充值；兼容端点: 视平台而定 | 视情况而定 |
| 智谱 BigModel API Key | 搜索/阅读/分析 MCP | open.bigmodel.cn | 有免费额度 | 推荐 |
| MinerU OpenXLab Key | PDF 云端转换 | openxlab.org.cn | 免费 | 可选 |

> **关于 Anthropic API Key**：如果你使用 Anthropic 官方 Claude Code，需要 Anthropic API Key。如果你通过 Anthropic 兼容端点（如智谱 BigModel）运行 Claude Code，则使用对应平台的 API Key 并配置 `base_url` 即可，无需 Anthropic API Key。

---

## 1. Anthropic API Key（或兼容端点 Key）

### 1.1 用途

Claude Code 需要一个 API Key 来调用 AI 模型。你可以选择：

- **Anthropic 官方 API Key**：直接调用 Anthropic 的 Claude 模型。
- **兼容端点 API Key**：通过 Anthropic 兼容端点（如智谱 BigModel GLM 系列、OpenRouter 等）运行，使用对应平台的 API Key 和 `base_url`。

所有 Skill 和 MCP 工具的 AI 推理能力都依赖此 Key。

> **注意**：如果使用兼容端点，以下注册和充值步骤不适用，请直接跳到 [1.5 配置](#15-配置) 部分。

### 1.2 注册步骤（仅 Anthropic 官方）

1. 打开浏览器，访问 [https://console.anthropic.com](https://console.anthropic.com)
2. 点击页面右上角的 **Sign Up** 按钮
3. 选择注册方式：
   - 使用 Google 账号登录（推荐）
   - 使用邮箱注册
4. 完成邮箱验证（如果使用邮箱注册）
5. 登录后进入控制台主页

### 1.3 创建 API Key（仅 Anthropic 官方）

1. 在控制台左侧菜单中，点击 **API Keys**
2. 点击 **Create Key** 按钮
3. 输入 Key 的名称（如 `claude-code-work`），便于后续管理
4. 复制生成的 Key（格式为 `sk-ant-api03-...`）
5. **重要**：Key 只显示一次，请立即保存到安全位置

### 1.4 充值（仅 Anthropic 官方）

Anthropic API 采用预付费模式：

- **最低充值**：$5 USD
- **支付方式**：信用卡（Visa/Mastercard）或借记卡
- **充值路径**：控制台 → Settings → Billing → Add Credits

**费用估算**（供参考）：

| 使用场景 | 模型 | 预估单次费用 |
|----------|------|-------------|
| 论文审阅 | Claude Sonnet | $0.05 - $0.15 |
| 深度调研 | Claude Sonnet | $0.20 - $0.80 |
| 学术写作 | Claude Sonnet | $0.10 - $0.30 |
| 简单问答 | Claude Haiku | $0.01 - $0.03 |

$5 额度大约可以支持 30-50 次论文审阅或 5-10 次深度调研。

### 1.5 配置

Claude Code 在首次启动时会提示输入 API Key。也可以通过环境变量配置：

**方式一：交互式输入**（推荐）

```bash
claude
# 首次启动时会提示：Enter your Anthropic API Key:
# 粘贴你的 Key 即可
```

**方式二：环境变量（Anthropic 官方）**

在 `~/.bashrc` 或 `~/.bash_profile` 中添加：

```bash
export ANTHROPIC_API_KEY="sk-ant-api03-your-key-here"
```

**方式三：环境变量（兼容端点，如智谱 BigModel）**

如果你使用 Anthropic 兼容端点，需要同时设置 API Key 和 base_url：

```bash
export ANTHROPIC_API_KEY="你的兼容端点API密钥"
export ANTHROPIC_BASE_URL="https://open.bigmodel.cn/api/paas/v4/"  # 以智谱为例
```

> 其他兼容端点（如 OpenRouter、AWS Bedrock 等）也支持类似配置，只需替换对应的 API Key 和 base_url。

然后执行：

```bash
source ~/.bashrc
```

### 1.6 验证

```bash
# 方法一：直接启动 Claude Code
claude
# 如果能正常对话，说明 Key 有效

# 方法二（仅 Anthropic 官方）：通过 API 测试
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 100,
    "messages": [{"role": "user", "content": "Hello"}]
  }'
# 返回 JSON 响应说明 Key 有效

# 方法二（兼容端点）：curl 测试对应端点
# 以智谱 BigModel 为例：
curl -X POST https://open.bigmodel.cn/api/paas/v4/chat/completions \
  -H "Authorization: Bearer $ANTHROPIC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "glm-5",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
# 返回 JSON 响应说明 Key 有效
```

---

## 2. 智谱 BigModel API Key

### 2.1 用途

智谱 BigModel API Key 用于以下 MCP 服务器：

| MCP 服务器 | 功能 |
|------------|------|
| `web-search-prime` | 网络搜索，获取最新网页信息 |
| `web-reader` | 网页内容抓取与 Markdown 转换 |
| `zread` | GitHub 仓库代码阅读和搜索 |
| `zai-mcp-server` | 图像/视频分析、截图 OCR |

这四个 MCP 服务器共用同一个 Key，配置一次即可全部使用。

### 2.2 注册步骤

1. 打开浏览器，访问 [https://open.bigmodel.cn](https://open.bigmodel.cn)
2. 点击页面右上角的 **注册/登录**
3. 选择注册方式：
   - 手机号注册（推荐，中国大陆用户）
   - 微信扫码注册
4. 完成手机号验证码验证
5. 登录后进入控制台

### 2.3 创建 API Key

1. 登录后，在控制台首页找到 **API Keys** 或 **密钥管理**
2. 点击 **创建新密钥** 按钮
3. 输入密钥名称（如 `claude-toolkit`）
4. 复制生成的 Key（格式为 `xxxxxxxx.xxxxxxxx`）
5. 保存到安全位置

### 2.4 费用与免费额度

智谱 BigModel 提供免费额度：

| 模型 | 免费额度 | 说明 |
|------|----------|------|
| GLM-4V-Flash | 免费调用 | 图像理解，web-search-prime 和 zai 使用 |
| GLM-4-Flash | 免费调用 | 文本生成，web-reader 使用 |
| 其他模型 | 按量计费 | 高级功能可能需要付费 |

> **注意**：免费额度有速率限制（QPS），对于深度调研的密集调用可能偶尔触发限流。日常使用免费额度完全足够。

### 2.5 配置

在 `~/.claude.json`（全局）或项目级 `.claude.json` 的 MCP 服务器配置中添加 Key：

```jsonc
{
  "mcpServers": {
    "web-search-prime": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-web-search-prime"],
      "env": {
        "BIGMODEL_API_KEY": "你的智谱API密钥"
      },
      "type": "stdio"
    },
    "web-reader": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-web-reader"],
      "env": {
        "BIGMODEL_API_KEY": "你的智谱API密钥"
      },
      "type": "stdio"
    }
  }
}
```

**提示**：如果多个 MCP 服务器使用同一个 Key，需要分别配置 `env` 字段。

### 2.6 验证

在 Claude Code 中执行：

```
请用 web-search-prime 搜索 "Claude Code MCP 配置"
```

如果返回搜索结果（包含标题、链接、摘要），说明 Key 配置正确。

也可以通过 curl 直接测试：

```bash
curl -X POST https://open.bigmodel.cn/api/paas/v4/chat/completions \
  -H "Authorization: Bearer 你的API密钥" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "glm-4-flash",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

---

## 3. MinerU OpenXLab Key

### 3.1 用途

MinerU OpenXLab Key 用于 MinerU MCP 服务器的云端 PDF 转换功能。当本地转换资源不足或需要更高质量的转换结果时，会使用云端 API。

主要功能：
- PDF/PPT/Word 转 Markdown（云端高质量转换）
- OCR 识别（支持中英文混排）
- 表格提取
- 公式识别

### 3.2 注册步骤

1. 打开浏览器，访问 [https://openxlab.org.cn](https://openxlab.org.cn)
2. 点击页面右上角的 **注册**
3. 选择注册方式：
   - 手机号注册
   - GitHub 账号授权登录（推荐）
4. 完成实名认证（部分功能需要）
5. 登录后进入个人中心

### 3.3 获取 API Key

1. 登录 OpenXLab 后，进入 **个人中心** 或 **开发者设置**
2. 找到 **API Token** 或 **Access Key** 选项
3. 点击 **生成新 Token**
4. 复制生成的 Token
5. 保存到安全位置

### 3.4 费用

| 功能 | 费用 |
|------|------|
| 基础 PDF 转 Markdown | 免费 |
| OCR 识别 | 免费 |
| 高级格式转换 | 免费（有速率限制） |

MinerU 云端转换目前完全免费，但有每日调用次数限制（通常足够日常使用）。

### 3.5 配置

在 MCP 服务器配置中添加：

```jsonc
{
  "mcpServers": {
    "mineru-mcp": {
      "command": "python",
      "args": ["-m", "mineru_mcp"],
      "env": {
        "MINERU_API_KEY": "你的OpenXLab_Token",
        "USE_LOCAL_API": "false"
      },
      "type": "stdio"
    }
  }
}
```

> **注意**：如果设置 `USE_LOCAL_API` 为 `true`，则使用本地转换（不需要 Key，但需要本地安装 MinerU 的完整依赖）。本地模式对 GPU 要求较高。

### 3.6 验证

在 Claude Code 中执行：

```
请用 MinerU 的 parse_documents 解析以下 PDF：
文件路径：测试文件路径.pdf
```

如果返回 Markdown 格式的内容，说明配置正确。

---

## 4. 配置文件汇总

以下是完整的 MCP 服务器配置示例（包含所有 Key）：

```jsonc
// ~/.claude.json 或 项目级 .claude.json
{
  "mcpServers": {
    // 结构化推理（无需 API Key）
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-sequential-thinking"],
      "type": "stdio"
    },

    // 网络搜索（需要智谱 Key）
    "web-search-prime": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-web-search-prime"],
      "env": {
        "BIGMODEL_API_KEY": "你的智谱API密钥"
      },
      "type": "stdio"
    },

    // 网页抓取（需要智谱 Key）
    "web-reader": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-web-reader"],
      "env": {
        "BIGMODEL_API_KEY": "你的智谱API密钥"
      },
      "type": "stdio"
    },

    // 图像/视频分析（需要智谱 Key）
    "zai-mcp-server": {
      "command": "npx",
      "args": ["-y", "@anthropic/zai-mcp-server"],
      "env": {
        "BIGMODEL_API_KEY": "你的智谱API密钥"
      },
      "type": "stdio"
    },

    // GitHub 仓库阅读（需要智谱 Key）
    "zread": {
      "command": "npx",
      "args": ["-y", "@anthropic/zread"],
      "env": {
        "BIGMODEL_API_KEY": "你的智谱API密钥"
      },
      "type": "stdio"
    },

    // PDF 转换（需要 OpenXLab Key）
    "mineru-mcp": {
      "command": "python",
      "args": ["-m", "mineru_mcp"],
      "env": {
        "MINERU_API_KEY": "你的OpenXLab_Token",
        "USE_LOCAL_API": "false"
      },
      "type": "stdio"
    },

    // MemPalace 语义记忆（无需额外 Key）
    "mempalace": {
      "command": "conda",
      "args": [
        "run", "-n", "mempalace",
        "--no-banner",
        "python", "-m", "mempalace.mcp_server"
      ],
      "type": "stdio"
    }
  }
}
```

---

## 5. 故障排查

### 5.1 Anthropic API Key / 兼容端点问题

#### 问题：Claude Code 启动报 "Invalid API Key"

**原因**：Key 不正确或已过期。

**解决**：
1. 检查 Key 是否完整复制（Anthropic 官方 Key 以 `sk-ant-api03-` 开头；兼容端点 Key 格式可能不同）
2. 确认没有多余的空格或换行符
3. 如果使用 Anthropic 官方：在 [console.anthropic.com](https://console.anthropic.com) 检查 Key 状态
4. 如果使用兼容端点：确认 `ANTHROPIC_BASE_URL` 已正确设置，并且 API Key 格式符合对应平台要求
5. 如果 Key 已失效，创建新的 Key

#### 问题：报 "Insufficient credits" 或 "Rate limit exceeded"

**原因**：余额不足或调用频率过高。

**解决**：
1. 检查余额：控制台 → Settings → Billing
2. 充值至少 $5
3. 如果是速率限制，等待 1-2 分钟后重试
4. 考虑使用 Haiku 模型降低成本（修改 `~/.claude/settings.json` 中的模型配置）

#### 问题：网络超时 "Connection refused" 或 "Timeout"

**原因**：网络连接问题，可能是代理配置不正确。

**解决**：
1. 检查网络连接是否正常
2. 如果使用代理（如 Clash Verge），确保 `HTTP_PROXY` 和 `HTTPS_PROXY` 环境变量已设置
3. 确认代理规则中 `api.anthropic.com` 走直连或代理（根据你的网络环境）
4. 尝试关闭代理直连测试

### 5.2 智谱 BigModel API Key 问题

#### 问题：web-search-prime 搜索返回空结果

**原因**：Key 无效、额度用尽或网络问题。

**解决**：
1. 检查 Key 格式（应为 `xxxxxxxx.xxxxxxxx` 格式，包含一个点号）
2. 在 [open.bigmodel.cn](https://open.bigmodel.cn) 控制台检查用量
3. 检查 `~/.claude.json` 中对应 MCP 服务器的 `env.BIGMODEL_API_KEY` 是否正确
4. 重启 Claude Code 使配置生效

#### 问题：报 "Model not found" 或 "Permission denied"

**原因**：账户没有该模型的访问权限。

**解决**：
1. 确认账户已完成实名认证
2. 在控制台检查是否已开通对应模型的访问权限
3. 部分高级模型需要单独申请

#### 问题：MCP 服务器启动失败

**原因**：npx 安装包或 Node.js 环境问题。

**解决**：
1. 确认 Node.js 版本 >= 18：
   ```bash
   node --version
   ```
2. 手动安装 MCP 包：
   ```bash
   npm install -g @anthropic/mcp-web-search-prime
   ```
3. 检查 npm 全局路径是否在 PATH 中

### 5.3 MinerU OpenXLab Key 问题

#### 问题：PDF 转换返回错误

**原因**：Token 无效或云端服务暂时不可用。

**解决**：
1. 检查 Token 是否正确
2. 尝试使用本地模式（`USE_LOCAL_API=true`），但需要本地安装完整 MinerU：
   ```bash
   pip install mineru
   ```
3. 等待几分钟后重试（可能是服务端临时故障）

#### 问题：OCR 识别质量差

**原因**：未启用 OCR 或语言设置不正确。

**解决**：
1. 在 MCP 调用中启用 OCR：
   ```
   parse_documents(file_sources="xxx.pdf", enable_ocr=true, language="ch")
   ```
2. 对于英文论文，设置 `language="en"`
3. 对于中英混排，设置 `language="ch"`（中文模式对英文也有较好支持）

#### 问题：大型 PDF 转换超时

**原因**：文件过大，云端处理时间较长。

**解决**：
1. 使用 `page_ranges` 参数分批转换：
   ```
   parse_documents(file_sources="xxx.pdf", page_ranges="1-10")
   ```
2. 对于超过 50 页的文档，建议分批处理
3. 考虑使用本地模式处理大型文件

### 5.4 通用排查步骤

遇到任何 Key 相关问题时，按以下步骤排查：

1. **确认 Key 格式**：检查 Key 是否完整、无多余空格
2. **确认配置位置**：检查 Key 是写在 `~/.claude.json`（全局）还是项目级 `.claude.json` 中
3. **重启 Claude Code**：修改配置后需要重启 Claude Code 才能生效
4. **检查环境变量**：确认 `ANTHROPIC_API_KEY` 等环境变量正确设置；如果使用兼容端点，确认 `ANTHROPIC_BASE_URL` 也已设置
5. **查看 MCP 日志**：Claude Code 的 MCP 服务器日志通常在 `~/.claude/logs/` 目录中
6. **网络检查**：确认可以访问对应的 API 端点（curl 测试）

---

## 6. 安全最佳实践

1. **永远不要**将 API Key 提交到 Git 仓库。确保 `.gitignore` 中包含：
   ```
   .env
   *.key
   *_credentials*
   ```

2. **使用环境变量**而非硬编码。推荐在 `~/.bashrc` 中设置 Key，然后在 `~/.claude.json` 中引用：
   ```bash
   # ~/.bashrc
   export ANTHROPIC_API_KEY="sk-ant-api03-..."  # 或兼容端点的 Key
   # 如果使用兼容端点（如智谱 BigModel），还需要设置：
   # export ANTHROPIC_BASE_URL="https://open.bigmodel.cn/api/paas/v4/"
   export BIGMODEL_API_KEY="xxxxxxxx.xxxxxxxx"
   export MINERU_API_KEY="your-openxlab-token"
   ```

3. **定期轮换 Key**：建议每 3-6 个月更换一次 API Key

4. **最小权限原则**：每个 Key 只赋予必要的权限

5. **监控用量**：定期检查各平台的用量面板，及时发现异常调用
