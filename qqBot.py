import asyncio
import websockets
import json
import socket
import requests

import os
import subprocess
import time

from local_chat import *

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

def sendMessage(userID, userName, user_message): 
    url = "http://127.0.0.1:3000/send_private_msg"
    reply = qq_chat(user_message)

    data = {
        "user_id": userID,
        "message": reply
    }

    try:
        response = requests.post(
            url,
            json=data,
            timeout=5
        )

        print("[AI]MahiroAIChat(3453211161) 向 ", userName, " (", userID, ") 发送消息\n", reply, sep='')
        print("======================")

    except Exception as e:  # 捕获异常
        print("发送失败:", e)


# =======================
# 作为服务端，等待 NapCat 客户端连接
# =======================

async def handler(websocket):

    print("NapCat 连接成功！")

    try:
        async for message in websocket:
            data = json.loads(message)

            # 只处理 message 聊天消息
            if (data.get("post_type") == "message"):
                userID = data.get("user_id")
                senderUserName = data["sender"]["nickname"]
                msg = data["message"][0]["data"]["text"]

                print("======================")
                print("[AI]MahiroAIChat(3453211161) 收到来自 ", senderUserName, "(", userID, ") 的消息", sep = '')
                print(msg)
                print("======================")

                sendMessage(userID, senderUserName, msg)

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