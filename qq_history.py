import os
import json

HISTORY_DIR = "qq_history" 

os.makedirs(       # 创建存储聊天记录目录
    HISTORY_DIR,
    exist_ok=True,
)

def getHistory(userID):
    path = os.path.join(HISTORY_DIR, f"{userID}.json")

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []

def saveHistory(userID, history):
    path = os.path.join(HISTORY_DIR, f"{userID}.json")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)
