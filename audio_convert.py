import pysilk   # 进行silk-v3语音解码
import os
import wave     # 处理wav的库

def audioConvert(audioPath):
    # 给定路径，实现silk->pcm->wav转换，返回路径

    # 第一步 获取pcm和wav的路径
    pcmPath = os.path.splitext(audioPath)[0] + ".pcm"
    wavPath = os.path.splitext(audioPath)[0] + ".wav"

    # 第二步 silk转换为pcm
    with open(audioPath, "rb") as silk, open(pcmPath, "wb") as pcm:
        pysilk.decode(silk, pcm, 24000)     # 24000是采样率

    # 第三步 pcm转换为wav
    with open(pcmPath, "rb") as pcm:
        pcmData = pcm.read()    # 读取pcm数据
    
    with wave.open(wavPath, "wb") as wav:
        wav.setnchannels(1)     # 单声道
        wav.setsampwidth(2)     # 采样宽度
        wav.setframerate(24000) # 采样率
        wav.writeframes(pcmData)    # 写入数据
    
    return wavPath

