import os

# 路径配置
MODEL_DIR = "D:/MahiroAIChat"
os.environ["MODELSCOPE_CACHE"] = MODEL_DIR

# ============================================
import gradio as gr
import time
from faster_whisper import WhisperModel

# ===================加载模型===================
print("加载语音识别模型中……")

sttModel = WhisperModel(
    "D:/MahiroAIChat/whisper_model_small",
    device="cuda",  # 走GPU
    compute_type="float16",
)

print("语音模型加载完毕。")


# ===================识别===================

def speechToText(audioPath):
    sentence, info = sttModel.transcribe(
        audioPath,
        language = "zh",
        beam_size = 5
    )     # 该函数返回整句话（sentence）和调试信息（info）

    result = ""
    for segment in sentence:
        print(segment.text)
        result += segment.text

    return result