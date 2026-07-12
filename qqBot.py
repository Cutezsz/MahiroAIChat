import asyncio
import websockets
import json
import socket
import requests

import os
import subprocess
import time

from const_define import *
from local_chat import *
from audioConvert import *      # 将 qq 语音转换为标准 wav 格式
from speech_to_text import *    # 处理 qq 语音

# =======================
# 启动 NapCat
# =======================

def startNapCat():
    workdir = os.path.join(
        "NapCat",
        "NapCat.44498.Shell",
    )       # 添加bat路径

    subprocess.Popen(       # 启动新的子进程
        ["cmd", "/k", "napcat.quick.bat"],
        cwd=workdir     # 设置工作目录
    )       # 启动 NapCat

# =======================
# 等待 NapCat 启动成功
# =======================

def waitNapCatStarting(host, port, maxWaitingTime):
    startTime = time.time()

    while True:
        if (time.time() - startTime > maxWaitingTime):
            raise TimeoutError("等待超时，请检查是否正确安装了 NapCat……")

        try:        # 创建一个 socket 连接，监测是否超时
            s = socket.create_connection((host, port), timeout=1)
            s.close()
            break
        except:
            time.sleep(1)

# =======================
# 作为服务端，向 NapCat 发送消息
# =======================

def sendMessage(userID, userName, reply): 
    url = "http://127.0.0.1:3000/send_private_msg"

    data = {
        "user_id": userID,
        "message": reply
    }

    try:
        print("向 ", userName, "(", userID, ") 发送消息\n", reply, sep='')
        print("======================")

        response = requests.post(
            url,
            json=data,
            timeout=5
        )

    except Exception as e:  # 捕获异常
        print("发送失败:", e)

# =======================
# 作为客户端，等待 NapCat 客户端连接
# =======================

async def handler(websocket):

    print("NapCat 连接成功！")
    sendMessage(951255007, "Cute_zsz", QQWelcome)

    try:
        async for message in websocket:
            data = json.loads(message)
            #print("JSON 数据：", data)

            # 只处理 message 聊天消息
            if (data.get("post_type") == "message"):
                userID = data.get("user_id")
                senderUserName = data["sender"]["nickname"]

                messageType = ''
                if (data["message"][0]["type"] == "text"): 
                    messageType = "文本消息"
                    msg = data["message"][0]["data"]["text"]
                elif (data["message"][0]["type"] == "record"):
                    messageType = "语音消息"
                    audioPath = data["message"][0]["data"]["path"]

                    # 等待语音文件下载
                    for _ in range(50):
                        if os.path.exists(audioPath):
                            break
                        time.sleep(0.1)
                    else:
                        print("语音文件下载失败，请检查网络连接。")
                        continue

                    wavPath = audioConvert(audioPath)
                    msg = speechToText(audioPath=wavPath)
                else: 
                    sendMessage(userID, senderUserName, QQMessageTypeError)
                    continue
                    

                print("======================")
                print("收到来自 ", senderUserName, "(", userID, ") 的", messageType, sep = '')
                print(msg)
                print("----------------------")

                sendMessage(userID, senderUserName, qq_chat(msg))

    except websockets.exceptions.ConnectionClosed:
        print("NapCat 断开连接……")


async def main():
    startNapCat()       # 启动 NapCat
    waitNapCatStarting("127.0.0.1", "3000", 60)    # 等待 http server 启动完成再进行

    server = await websockets.serve(
        handler,        # 调用 handler
        "127.0.0.1",
        8080
    )

    print("QQ机器人 WebSocket 服务器启动。")
    print("监听中 ws://127.0.0.1:8080")

    await server.wait_closed()


asyncio.run(main())