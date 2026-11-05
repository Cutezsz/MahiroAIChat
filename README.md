# MahiroAIChat

一个以《别当欧尼酱了！》中的**绪山真寻**为人设的 AI 聊天机器人。支持文本与语音对话，可通过 QQ（私聊 / 群聊）和 Gradio Web 界面使用，具备**联网搜索、主动思考、图像识别、群聊自主接话**等 Agent 能力。

> 项目起源于一个暑假的兴趣：给自己做一个“赛博女儿”。目前仍在持续迭代中。

---

## ✨ 功能特性

### 对话与角色扮演
- **角色人设**：基于《别当欧尼酱了！》中的绪山真寻，人设文件外置为 `mahiro.md`，可独立编辑和迭代。
- **多轮对话**：支持上下文记忆，私聊与群聊分别维护独立的历史记录。
- **文本与语音**：QQ 消息支持文本和语音输入，语音通过 Faster-Whisper 转写后进入对话流程。

### Agent 能力（V2.2+）
- **联网搜索**：模型可在需要时调用 `webSearch` 工具（Tavily API）获取实时信息，并用真寻的语气转述结果。
- **主动思考**：模型可在遇到需要推理、比较、权衡的问题时调用 `think` 工具，开启 DeepSeek 的思考模式获得结论，再回到快速模式生成最终回复。
- **工具调用循环**：基于 DeepSeek Tool Calls 实现，最多循环 `MAX_TOOL_ROUNDS` 轮，防止死循环。

### 图像识别（V2.3+）
- QQ 图片消息会通过 `deepseek_image.py` 送入视觉模型进行描述或识别，结果拼入对话上下文。
- 针对角色识别精度问题，采用了“先拆解特征（发色、瞳色、发型、配饰）再判断”的提示策略，并允许模型在不确定时回答“认不出”而非硬猜。

### 群聊主动接话（V2.3+）
- 群消息会先写入历史，然后通过 `judgeActive()` 让模型输出一个 `0~1` 的浮点数，判断是否应该主动接话。
- 配合**冷却时间**（`ACTIVE_COOLDDOWN`）和**分数阈值**（`ACTIVE_CHAT_THRESHOLD`），避免频繁插嘴。
- @ 消息走独立短路逻辑，不经过主动判断层。

### 部署与界面
- **QQ 机器人**：通过 NapCat + OneBot11 协议接入，支持反向 WebSocket。
- **Web 界面**：Gradio 界面用于本地调试和对话测试。
- **历史持久化**：聊天记录以 JSON 格式按用户 / 群组分别存储。

---

## 🧱 技术栈

| 类别 | 选型 |
| :--- | :--- |
| 语言 | Python 3.12 |
| 对话模型 | DeepSeek V4（`deepseek-v4-flash`） |
| 视觉模型 | `deepseek-flash`（视觉输入） |
| 搜索工具 | Tavily API |
| 语音转文字 | Faster-Whisper |
| QQ 接入 | NapCat + OneBot11 |
| Web 界面 | Gradio |
| 本地模型（可选） | Qwen2.5-1.5B-Instruct（4bit 量化） |

> 项目早期版本基于本地 Qwen2.5-1.5B-Instruct，V2.0 起接入 DeepSeek API，本地模型路径保留作为离线或降级方案。

---

## 📁 项目结构（核心文件）

```text
MahiroAIChat/
├── const_define.py       # 全局常量：模型参数、阈值、路径等
├── mahiro.md             # 真寻人设文件（Markdown，可独立编辑）
├── deepseek_chat.py      # DeepSeek 对话 + Agent 工具调用循环
├── deepseek_image.py     # 图像识别（视觉模型调用）
├── tools.py              # Agent 工具定义与执行（webSearch / think）
├── qq_bot.py             # QQ 机器人主逻辑（消息处理、群聊判断）
├── qq_history.py         # 聊天历史存取（JSON）
├── qqUsers.py            # QQ 用户列表管理
├── audioConvert.py       # QQ silk 语音 → PCM → WAV
├── speech_to_text.py     # Faster-Whisper 语音转文字
├── local_chat.py         # 本地 Qwen 模型聊天逻辑（降级 / 离线）
├── gui.py                # Gradio Web 界面
└── README.md
```

> 本仓库不包含模型权重，仅存储源代码。

---

## 🚀 快速开始

### 环境要求
- Python 3.12+
- 可用的 DeepSeek API Key
- 可用的 Tavily API Key（搜索功能）
- NapCat（QQ 接入）

### 安装依赖

```bash
pip install openai tavily-python faster-whisper gradio requests beautifulsoup4 pysilk
```

> 本地模型路径（Qwen2.5-1.5B-Instruct）需要额外安装 `torch`、`transformers`、`accelerate`、`bitsandbytes`。

### 配置

在系统环境变量中配置：

```bash
DEEPSEEK_API_KEY=your_deepseek_key
TAVILY_API_KEY=your_tavily_key
```

人设文件 `mahiro.md` 可直接编辑，无需改动代码。

### 启动

1. **启动 NapCat**，配置反向 WebSocket 指向你的 Python 服务端（默认 `ws://localhost:8080`）。
2. **启动 QQ 机器人**：

```bash
python qq_bot.py
```

3. **或使用 Gradio 界面**：

```bash
python gui.py
```

---

## 🧭 版本演进

| 版本 | 核心变化 |
| :--- | :--- |
| **V1.1** | 语音聊天功能（silk → PCM → WAV + Faster-Whisper） |
| **V1.2** | 历史记忆功能（JSON 按用户 / 群组存储） |
| **V1.3** | 数据库更新（用户列表管理） |
| **V2.0** | 模型更新（接入 DeepSeek API，本地 Qwen 作为降级路径） |
| **V2.1** | 群聊天功能 |
| **V2.2** | **智能体（Agent）更新**：工具调用循环、`webSearch`、`think`、人设外置为 `mahiro.md` |
| **V2.3** | **图像处理**（视觉模型识图）+ **活跃聊天**（群聊主动接话判断 + 冷却机制） |

> 博客教程目前停留在 V2.1，V2.2 和 V2.3 的内容已在代码中实现，README 作为最新功能索引。

---

## ⚠️ 已知限制

- **视觉角色识别精度有限**：DeepSeek Flash 视觉模型在细粒度动漫角色识别上容易误认（例如把爱音识别为星野）。项目采用“先拆特征再判断”的提示策略缓解，但无法根治。
- **思考工具会增加延迟**：`think` 开启思考模式，单次调用可能需要数秒到数十秒，群聊场景建议配合冷却或按需启用。
- **QQ 账号风控**：NapCat 登录可能触发腾讯风控，建议使用稳定的网络环境，首次登录手动扫码建立缓存后再尝试快速登录。

---

## 📄 版权

Copyright © 2026 Cute_zsz. All rights reserved.
