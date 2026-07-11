import asyncio
import websockets
import json
import requests

from local_chat import *

# =======================
# 作为客户端，向 NapCat 发送消息
# =======================

def sendMessage(userID, user_message): 
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

        print("成功发送回复消息", reply)
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
                print("Fake_zsz(3453211161) 收到来自 ", senderUserName, "(", userID, ") 的消息", sep = '')
                print(msg)
                print("======================")

                sendMessage(
                    userID, 
                    "收到了喵~"
                )

    except websockets.exceptions.ConnectionClosed:
        print("NapCat 断开连接")


async def main():

    server = await websockets.serve(
        handler,
        "127.0.0.1",
        8080
    )

    print("QQ机器人 WebSocket 服务器启动")
    print("监听中 ws://127.0.0.1:8080")

    await server.wait_closed()


asyncio.run(main())