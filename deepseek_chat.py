import os
from openai import OpenAI
from const_define import *

client = OpenAI(
    api_key = os.environ["DEEPSEEK_API_KEY"],       # 获取api
    base_url = "https://api.deepseek.com/"
)

def deepseekChat(user_message, history, isThinking = False):
    history = history or []
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    for message in history:
        messages.append(message)

    messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    response = client.chat.completions.create(
        model = 'deepseek-v4-flash',        # 聊天用flash模型
        messages = messages,
        temperature = TEMPERATURE, 
        max_tokens= MAX_NEW_TOKENS,
        top_p = TOP_P,
        stream = False
    )

    finish_reason = response.choices[0].finish_reason
    if (finish_reason == "stop"):       # 正常情况
        return response.choices[0].message.content
    elif (finish_reason == "length"):   # 长度限制
        return f"【ERROR】回答生成超过长度限制（Generated Reply Exceeded）"