# ChangeToABetterLife

**每日任务追踪 + AI 复盘分析 = 改变人生的第一步**

A gamified daily task tracker with AI-powered journaling and analysis. Track your tasks, review your day, and get honest feedback from AI to build better habits.

## Setup / 安装

```bash
pip install -r requirements.txt
```

## Run / 运行

```bash
python server.py
```

Then open **http://localhost:9527** in your browser (or just open `index.html` directly).

## API Key / 获取密钥

You need an API key from one of:

- **Anthropic (Claude)**: https://console.anthropic.com
- **OpenAI (GPT)**: https://platform.openai.com

Click the ⚙ gear icon in the bottom-right corner of the app to enter your key.

Alternatively, set environment variables: `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`.

## Features / 功能

- **Task Tracking** — 添加、完成、删除每日任务
- **Pomodoro Timer** — 30/60/90 分钟专注模式
- **Daily Review** — 写下今天做了什么，AI 帮你分析
- **AI Scoring** — 1-4 分制评估你的一天 (摧毁人生 → 正在进化)
- **21-Day Heatmap** — 可视化你的近期表现
- **Trend Analysis** — AI 分析多日趋势和习惯
- **Smart Suggestions** — AI 根据历史推荐今日任务
- **Journal Export** — 导出所有日记记录
- **Settings Panel** — 在浏览器中配置 API Key，无需环境变量
