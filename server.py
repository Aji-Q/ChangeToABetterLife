# -*- coding: utf-8 -*-
# ChangeToABetterLife - AI Analysis Server
# Start: python server.py
# Requires: pip install flask flask-cors anthropic openai

import os
import sys
import io
import json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Fallback: load API key from environment or OpenClaw config
def _load_api_key_from_env():
    import pathlib
    key = os.environ.get('ANTHROPIC_API_KEY', '')
    if key:
        return key
    try:
        cfg = pathlib.Path.home() / '.openclaw' / 'agents' / 'manager' / 'agent' / 'auth-profiles.json'
        data = json.loads(cfg.read_text(encoding='utf-8'))
        token = data.get('profiles', {}).get('anthropic:default', {}).get('token', '')
        if token:
            return token
    except Exception:
        pass
    return ''

ANALYZE_PROMPT = (
    "You are a concise productivity coach analyzing a student's day. "
    "Be direct, specific, and practical. No fluff. Respond in Chinese. "
    "Format your response with these three sections:\n"
    "[时间分析] Estimate time breakdown based on what they wrote (2-3 sentences)\n"
    "[做得好的] 1-2 things that went well today (be specific)\n"
    "[明日建议] 2-3 specific actionable improvements for tomorrow\n"
    "Keep each section to 2-3 sentences max. Be honest and a bit blunt.\n\n"
    "After the three sections, on a NEW LINE, output exactly: SCORE:X\n"
    "where X is 1, 2, 3, or 4 based on overall day quality:\n"
    "1 = 正在摧毁人生: Mostly wasted (heavy gaming/phone, no study, no sleep discipline)\n"
    "2 = 混日子: Mixed/mediocre (some productive, some wasteful, nothing exceptional)\n"
    "3 = 老老实实生活: Solid day (mostly productive, minor issues)\n"
    "4 = 正在进化: Excellent (strong focus, good habits, clear progress)\n"
    "Be honest. 6h gaming + 1h study = score 1 or 2, NOT 4. Judge by actual time allocation."
)

TREND_PROMPT = (
    "You are a blunt but caring coach. Analyze this student log history. "
    "Look for patterns: sleep, gaming, study time, mood. "
    "Identify concrete trends. Be specific with data (e.g. average gaming hours decreased from 6 to 4 over the week). "
    "If overall trend is negative, issue a clear warning. If positive, give specific praise. "
    "Respond in Chinese, keep it under 200 words, be direct."
)

SUGGEST_PROMPT = (
    "Based on this student log history, generate 3-4 specific, personalized task suggestions for today. "
    "Be concrete and reference their actual patterns (e.g. if they game 6h daily, suggest gaming time limit). "
    "Each suggestion should be 1 short sentence, actionable, specific. "
    "Output as JSON array of strings. Respond in Chinese. "
    "Example output: [\"今天把游戏时间控制在3小时以内\", \"下午做完数学卷子再开手机\", \"晚上11点前上床\"]"
)


def _call_ai(system_prompt, user_content, max_tokens=600, api_key='', provider=''):
    """Unified AI call. Uses provided api_key/provider first, then falls back to env."""

    # Determine which provider/key to use
    anthropic_key = ''
    openai_key = ''

    if api_key:
        if provider == 'openai':
            openai_key = api_key
        else:
            # Default to anthropic
            anthropic_key = api_key

    # Fallback to environment
    if not anthropic_key:
        anthropic_key = os.environ.get('ANTHROPIC_API_KEY', '') or _load_api_key_from_env()
    if not openai_key:
        openai_key = os.environ.get('OPENAI_API_KEY', '')

    if anthropic_key and provider != 'openai':
        import anthropic
        client = anthropic.Anthropic(api_key=anthropic_key)
        message = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_content}]
        )
        return message.content[0].text

    if openai_key:
        import openai
        client = openai.OpenAI(api_key=openai_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ]
        )
        return response.choices[0].message.content

    return None


@app.route('/api/analyze', methods=['POST', 'OPTIONS'])
def analyze():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    data = request.get_json(force=True)
    text = data.get('text', '').strip()
    tasks_done = data.get('tasks_done', [])
    tasks_total = data.get('tasks_total', [])
    api_key = data.get('api_key', '')
    provider = data.get('provider', '')

    if not text:
        return jsonify({'error': '请填写今日复盘内容'}), 400

    context = f"今日完成任务: {len(tasks_done)}/{len(tasks_total)}\n用户复盘: {text}"

    try:
        result = _call_ai(ANALYZE_PROMPT, context, api_key=api_key, provider=provider)
        if result is None:
            return jsonify({'error': '未找到 API Key，请在设置中填入你的 API Key'}), 500
        # Parse SCORE:X from end of response
        import re
        score = 2  # default: 混日子
        clean = result
        m = re.search(r'\bSCORE:([0-4])\b.*', result, re.DOTALL)
        if m:
            score_raw = int(m.group(1))
            score = max(1, score_raw)  # treat 0 as 1
            clean = result[:m.start()].rstrip()
        return jsonify({'result': clean, 'score': score})
    except Exception as e:
        return jsonify({'error': f'API error: {str(e)}'}), 500

@app.route('/api/trend', methods=['POST', 'OPTIONS'])
def trend():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    data = request.get_json(force=True)
    logs = data.get('logs', [])
    api_key = data.get('api_key', '')
    provider = data.get('provider', '')

    if not logs:
        return jsonify({'error': '没有足够的日志数据'}), 400

    # Build context from logs
    lines = []
    for log in logs:
        date = log.get('date', '?')
        text = log.get('text', '无记录')
        total = log.get('tasksTotal', 0)
        done = log.get('tasksDone', 0)
        lines.append(f"[{date}] 任务完成: {done}/{total} | 复盘: {text}")

    context = "\n".join(lines)

    try:
        result = _call_ai(TREND_PROMPT, context, max_tokens=400, api_key=api_key, provider=provider)
        if result is None:
            return jsonify({'error': '未找到 API Key'}), 500
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': f'API error: {str(e)}'}), 500

@app.route('/api/suggest', methods=['POST', 'OPTIONS'])
def suggest():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    data = request.get_json(force=True)
    logs = data.get('logs', [])
    api_key = data.get('api_key', '')
    provider = data.get('provider', '')

    if not logs:
        return jsonify({'suggestions': []}), 200

    lines = []
    for log in logs:
        date = log.get('date', '?')
        text = log.get('text', '无记录')
        lines.append(f"[{date}] {text}")

    context = "\n".join(lines)

    try:
        result = _call_ai(SUGGEST_PROMPT, context, max_tokens=300, api_key=api_key, provider=provider)
        if result is None:
            return jsonify({'suggestions': []}), 200

        # Parse JSON from AI response
        import re
        match = re.search(r'\[.*\]', result, re.DOTALL)
        if match:
            suggestions = json.loads(match.group())
            if isinstance(suggestions, list):
                return jsonify({'suggestions': [s for s in suggestions if isinstance(s, str)][:4]})

        return jsonify({'suggestions': []}), 200
    except Exception:
        return jsonify({'suggestions': []}), 200

@app.route('/health', methods=['GET'])
def health():
    has_key = bool(os.environ.get('ANTHROPIC_API_KEY') or os.environ.get('OPENAI_API_KEY'))
    return jsonify({'status': 'ok', 'api_key_configured': has_key})

if __name__ == '__main__':
    print("=" * 44)
    print("  ChangeToABetterLife - Analysis Server")
    print("  http://localhost:9527")
    print("=" * 44)
    has_key = bool(os.environ.get('ANTHROPIC_API_KEY') or os.environ.get('OPENAI_API_KEY'))
    if has_key:
        print("  API key (env): OK")
    else:
        print("  No env API key — users can set key in browser settings")
    app.run(host='0.0.0.0', port=9527, debug=False)
