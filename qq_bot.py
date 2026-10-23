import asyncio
import websockets
import json
import socket
import requests

import os
import subprocess
import time

# 做项目尽量不要全导入，按需导入
from const_define import *
from audio_convert import audioConvert      # 将 qq 语音转换为标准 wav 格式
from speech_to_text import speechToText    # 处理 qq 语音
from qq_history import saveHistory, getHistory         # 处理 qq 聊天记录
from qq_users import addUser, getQQUsers           # 获取 qq 用户列表
from deepseek_chat import deepseekChat     # 接入 deepseek 作为聊天 api

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

def sendPrivateMessage(userID, userName, reply): 
    url = "http://127.0.0.1:3000/send_private_msg"

    data = {
        "user_id": userID,
        "message": reply
    }

    try:
        print("向用户 ", userName, "(", userID, ") 发送消息\n", reply, sep='')
        print("======================")

        response = requests.post(
            url,
            json=data,
            timeout=5
        )

    except Exception as e:  # 捕获异常
        print("发送失败:", e)

def sendGroupMessage(groupID, groupName, reply):
    url = "http://127.0.0.1:3000/send_group_msg"

    data = {
        "group_id": groupID,
        "message": reply
    }

    try:
        print("向群聊 ", groupName, "(", groupID, ") 发送消息\n", reply, sep='')
        print("======================")

        response = requests.post(
            url,
            json=data,
            timeout=5
        )

    except Exception as e:
        print("发送失败:", e)

# =======================
# 开启之后向所有用户发送消息
# =======================

def ohayo():
    users = getQQUsers()
    for user in users:
        if (user["id"] != 951255007):
            reply = deepseekChat("你好呀！", [], isThinking = False)
            sendPrivateMessage(user["id"], user["name"], reply)

# =======================
# 作为客户端，等待 NapCat 客户端连接
# =======================

async def handler(websocket):

    print("NapCat 连接成功！")
    # ohayo()
    sendPrivateMessage(951255007, "Cute_zsz", QQWelcome)

    try:
        async for message in websocket:
            data = json.loads(message)
            # print("JSON 数据：", data)

            # 私聊
            if (data.get("message_type") == "private"):
                if (data.get("post_type") != "message"): continue
                userID = data.get("user_id")
                senderUserName = data["sender"]["nickname"]
                addUser(userID, senderUserName)     # 收到消息时添加用户

                # 处理消息
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
                    sendPrivateMessage(userID, senderUserName, QQMessageTypeError)
                    continue

                # 日志
                print("======================")
                print("收到来自 ", senderUserName, "(", userID, ") 的", messageType, sep = '')
                print(msg)
                print("----------------------")

                history = getHistory(userID)
                # reply = qq_chat(msg, history)
                reply = deepseekChat(msg, history)  # 调用deepseek聊天

                # 保存历史记录
                history.append(
                    {
                        "role": "user",
                        "content": msg
                    }
                )
                history.append(
                    {
                        "role": "assistant",
                        "content": reply
                    }
                )

                history = history[-MAX_HISTORY:]     # 只保留最近的 MAX_HISTORY 条记录
                saveHistory(userID, history)
                sendPrivateMessage(userID, senderUserName, reply=reply)

            # 群聊
            if (data.get("message_type") == "group"):
                if (data.get("post_type") != "message"): continue
                groupID = data.get("group_id")
                groupName = data.get("group_name")
                role = data["sender"]["role"]
                if (role == "owner"): role = "群主"
                if (role == "admin"): role = "管理员"
                if (role == "member"): role = "成员"
                
                userID = data.get("user_id")
                senderUserName = data["sender"]["nickname"]
                addUser(userID, senderUserName)    

                # 获取@的位置以及是否@自己
                At = -1
                isSendToSelf = False
                for i in range(len(data["message"])):
                    if (data["message"][i]["type"] == "at"):
                        At = i
                        isSendToSelf = (data["message"][i]["data"]["qq"] == str(SELF_QQ_ID))

                messageType = ''
                msg = ''
                stop = False
                for i in range(len(data["message"])):
                    if (i == At): 
                        continue  # 跳过@消息

                    if (data["message"][i]["type"] == "text"): 
                        messageType = "文本消息"
                        msg += data["message"][i]["data"]["text"]
                    elif (data["message"][i]["type"] == "record"):
                        messageType = "语音消息"
                        audioPath = data["message"][i]["data"]["path"]

                        for _ in range(50):
                            if os.path.exists(audioPath):
                                break
                            time.sleep(0.1)
                        else:
                            print("语音文件下载失败，请检查网络连接。")
                            stop = True
                            break

                        wavPath = audioConvert(audioPath)
                        msg += speechToText(audioPath=wavPath)
                    else: 
                        pass        
                if (stop): continue


                print("======================")
                print("收到来自群 ", groupName, "(", groupID, ") 中 ", role, " ", senderUserName, "(", userID, ") 的", messageType, sep = '')
                print(msg)
                print("----------------------")

                # 对于不是@自己的消息，只需要存进群消息记录即可
                if (isSendToSelf == False):
                    history = getHistory(groupID, GROUP_HISTORY_DIR)
                    history.append(
                        {
                            "role": "user",
                            "content": senderUserName + "说：" + msg
                        }
                    )
                    saveHistory(groupID, history, GROUP_HISTORY_DIR)
                else: 
                    # 处理@自己的消息
                    groupHistory = getHistory(groupID, GROUP_HISTORY_DIR)
                    reply = deepseekChat(senderUserName + '说：' + msg, groupHistory)  # 调用deepseek聊天

                    # 写入新的历史记录
                    groupHistory.append(
                        {
                            "role": "user",
                            "content": senderUserName + "说：" + msg
                        }
                    )
                    groupHistory.append(
                        {
                            "role": "assistant",
                            "content": reply
                        }
                    )

                    groupHistory = groupHistory[-MAX_GROUP_HISTORY:]     # 只保留最近的 MAX_HISTORY 条记录
                    saveHistory(groupID, groupHistory, GROUP_HISTORY_DIR)
                    sendGroupMessage(groupID, groupName, reply)

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