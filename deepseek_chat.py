import os
import json

from openai import OpenAI
from const_define import (
    SYSTEM_PROMPT, TEMPERATURE, MAX_NEW_TOKENS, TOP_P, MAX_TOOL_ROUNDS,       # 基础参数
    REPLY_EXCEEDED, UNKNOWN_ERROR, TOOL_FALLBACK_REPLY      # 报错
)

from tools import *

client = OpenAI(
    api_key = os.environ["DEEPSEEK_API_KEY"],       # 获取api
    base_url = "https://api.deepseek.com/"
)

def deepseekChat(user_message, history):
    history = history or []
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += history
    messages.append({"role": "user", "content": user_message})

    for _ in range(MAX_TOOL_ROUNDS):
        response = client.chat.completions.create(
            model = 'deepseek-v4-flash',        # 聊天用flash模型
            messages = messages,
            temperature = TEMPERATURE, 
            max_tokens= MAX_NEW_TOKENS,
            top_p = TOP_P,
            stream = False, 
            extra_body={"thinking": {"type": "disabled"}},      # 显式不思考，让模型自己决定是否思考
            tools = TOOLS   # 模型可用的工具
        )
        msg = response.choices[0].message
        
        finish_reason = response.choices[0].finish_reason
        if finish_reason == "tool_calls":   # AI 需要调用工具
            messages.append(msg)
            for tool in msg.tool_calls:
                args = json.loads(tool.function.arguments)  # 参数
                result = execute(tool.function.name, args)
                messages.append({"role": "tool", "tool_call_id": tool.id, "content": result})
            continue
            
        if finish_reason == "stop":       # 正常情况
            return msg.content
        
        if finish_reason == "length":   # 长度限制
            return REPLY_EXCEEDED
        
        return UNKNOWN_ERROR
    
    return TOOL_FALLBACK_REPLY  # 调用太多次工具


def judgeActive(history):
    content = "\n".join(f"{m['role']}: {m['content']}" for m in history)

    response = client.chat.completions.create(
        model = "deepseek-flash",
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "阅读下面的上下文记录，仅给出一个介于 0 到 1 之间的浮点数，判断是否应该主动接话。"},
                    {"type": "text", "text": "如果记录内刚回复过用户类似的话题，则偏向于不回复；如果记录内用户提到了自己，如出现 AI、真寻、机器人这类的关键词，则偏向于回复。"},
                    {"type": "text", "text": content}
                ],
            },
        ],
    )

    return float(response.choices[0].message.content)