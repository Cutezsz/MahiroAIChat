import base64
import os
from openai import OpenAI

client = OpenAI(
    api_key = os.environ["DEEPSEEK_API_KEY"],       # 获取api
    base_url = "https://api.deepseek.com/"
)

def deepseekImage(url):
    response = client.chat.completions.create(
        model = "deepseek-flash",
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "这张图片里有什么？"},
                    {
                        "type": "image_url",
                        "image_url": {"url": url},
                    },
                ],
            },
        ],
    )

    return response.choices[0].message.content