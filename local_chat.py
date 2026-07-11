import os

# 多模块，导入文件
from const_define import *

# 路径配置
os.environ["MODELSCOPE_CACHE"] = MODEL_DIR
os.environ["HF_HOME"] = MODEL_DIR + "/huggingface"
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

import threading

import torch
import gradio as gr

from transformers import (
    AutoTokenizer,      # 文字变token
    AutoModelForCausalLM,   # 调用大模型
    BitsAndBytesConfig,     # 4bit量化配置
    TextIteratorStreamer,   # 流式输出
)

from speech_to_text import *
from gui import *
from replyGeneration import *

##########################################
# 模型
##########################################

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

SYSTEM_PROMPT = """
你是《别当欧尼酱了》里的绪山真寻。

人物设定：
- 原本是家里蹲哥哥。
- 被妹妹变成了女孩子。
- 性格有点懒散，偶尔吐槽。
- 很喜欢玩游戏和动画。
- 回答自然、可爱一点，时不时说话结尾带喵。
- 可以帮助主人 Cute_zsz 学习、编程、聊天。
"""

##########################################
# 4bit量化配置
##########################################

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,  # 加载时压缩成4bit
    bnb_4bit_quant_type="nf4",  # 采用nf4量化
    bnb_4bit_use_double_quant=True,     # 二次量化
    bnb_4bit_compute_dtype=torch.float16,
)

print("加载Tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
)

print("加载模型中...")

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
    device_map="auto",
    dtype=torch.float16,
)

model.eval()

print("模型加载完毕。")

##########################################
# 对话
##########################################

def chat(user_message, history):

    # 输出history
    print("="*60)
    print(history)
    print("="*60)
    
    history = history or []      # 如果history有值，则赋值给history，否则赋值为空列表
    
    # 第一步：处理messages
    messages = [        # 初始化messages
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]
    for message in history:
        messages.append(
            {
                "role": message["role"],
                "content": message["content"][0]["text"]
            }
        )
    messages.append(
        {
            "role": "user",
            "content": user_message,
        }
    )

    # 第二步：生成文本
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )
    inputs = tokenizer(
        text,
        return_tensors="pt",
    ).to(model.device)

    # 第三步：生成回答，流式输出
    history.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    history.append(
        {
            "role": "assistant",
            "content": ""
        }
    )

    for answer in replyGeneration(
            tokenizer=tokenizer, 
            model=model,    
            inputs=inputs,
            TextIteratorStreamer=TextIteratorStreamer,
            threading=threading
        ):
        history[-1]["content"] = answer      # 历史对话的最后一项的回答，等于现在已经生成的文本
        yield history       # 返回历史对话


##########################################
# 语音输入
##########################################

def mic_chat(audioPath, history):
    text = speechToText(audioPath)      # 进行识别
    yield from chat(text, history)      # 把结果交给chat函数

##########################################
# qq聊天回复
##########################################

def qq_chat(user_message):
    
    # 第一步：处理messages
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

    # 第二步：生成文本
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )
    inputs = tokenizer(
        text,
        return_tensors="pt",
    ).to(model.device)

    # 第三步：返回回答
    answer = ""
    for new_answer in replyGeneration(
            tokenizer=tokenizer,
            model=model,
            inputs=inputs,
            TextIteratorStreamer=TextIteratorStreamer,
            threading=threading
        ):
        answer = new_answer
    
    return answer

##########################################
# Gradio
##########################################

'''
demo = gr.ChatInterface(
    fn = chat,
    title = "绪山真寻·你的AI助手",
    description = "可以本地离线部署，基于《别当欧尼酱了》的主角绪山真寻的AI助手，由Qwen2.5-1.5B-Instruct模型驱动。",
)'''

GUI = createUI(chat, mic_chat)

GUI.launch(
    server_name="127.0.0.1",
    inbrowser=True,
    share = True
)

