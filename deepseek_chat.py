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
    return response.choices[0].message.content