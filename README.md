# ChangeToABetterLife

> **你不是懒。你只是没有一个真正会审判你的工具。**

大多数人知道自己在混日子。打开手机刷了3小时，然后合理化："今天累了，明天补。"

明天永远不来。

**ChangeToABetterLife** 是一个每日追踪 + AI 复盘工具。它不给你鸡汤，不给你勋章，不哄你开心。它只做一件事：**告诉你，你今天到底过了什么样的一天。**

---

## Requirements

- **Python 3.8+**
- Modern browser (Chrome / Edge / Firefox)
- Anthropic or OpenAI API key

---

## 快速开始 / Quick Start

```bash
# 1. 安装依赖 / Install dependencies
pip install -r requirements.txt

# 2. 启动服务 / Start server
python server.py

# 3. 打开浏览器 / Open browser
# http://localhost:9527

# 4. 点右下角 ⚙ → 输入你的 API Key
# Click ⚙ bottom-right → enter your API key
```

**获取 API Key / Get your API Key：**
- Anthropic (Claude)：https://console.anthropic.com
- OpenAI (GPT)：https://platform.openai.com

---

## 它能做什么 / Features

### 🎯 每日任务管理
写下今天必须完成的事。完成打勾，没完成就是没完成。没有借口的空间。

### ⏱ 专注计时器（Pomodoro）
三档模式，逼你选择：
- ⚡ **快冲 30m** — 拖延症发作时的最低门槛
- 💪 **深度 60m** — 正常工作节奏
- 🗿 **巨石 90m** — 真正想做成一件事的时候

没有自定义时长。因为"我设个45分钟"是你在找退路。

### 📓 每日复盘 + AI 分析
睡前写下今天做了什么：玩了几小时游戏、学了多少、运动没有。

AI 会分析你写的内容，然后给出：
- **时间分析**：你把时间花在哪了，比例是否合理
- **做得好的**：找到真实的亮点，不是空洞的表扬
- **明日建议**：具体的、可执行的下一步，不是废话

它会直接说："你的一天基本被原神占据了，6小时游戏 vs 1小时学习，时间分配极度失衡。"

### 📊 21天热力图 — 你的人生轨迹一眼看清
每天一个格子，颜色不说谎：

| 颜色 | 等级 | 意味着 |
|------|------|--------|
| ⬜ 白色 | 无记录 | 你甚至没有记录这一天 |
| 🔴 红色 | 正在摧毁人生 | 沉迷娱乐，几乎没有产出 |
| 🟠 橙色 | 混日子 | 活着，但没有在前进 |
| 🟢 绿色 | 老实生活 | 正常度过，有基本的自律 |
| 🩷 粉色 | **正在进化** | 这一天，你真的在变好 |

连续几天白格和红格——你会知道该怎么做。

### 🤖 AI 智能推荐
每天打开 app，AI 根据你过去几天的记录给出今日建议。不是通用模板，是真的看过你昨天"刷了7小时抖音"之后说："今天把手机时间压到2小时以内。"

### 📅 日记本
每一天的复盘、任务、AI分析都保存下来。点开历史任意一天，VIEW AI 按钮实时重新分析该天内容。导出全部记录为 `.txt` 文件。

---

## Screenshots

> Screenshots coming soon

---

## 数据说明

所有数据存储在你的浏览器本地（localStorage）。没有服务器，没有账户，没有人看你的记录。**只有你自己知道你过了什么样的一天。**

---

## 写在最后

这个工具不会让你变好。

**你的行动才会。**

但至少，它会让你没法再对自己撒谎。

---

## License

MIT

---

*Made with frustration and too many wasted evenings.*
*如果这个工具帮到了你，给个 ⭐ Star 就是最好的反馈。*
