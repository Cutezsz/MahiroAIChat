import os
import json
from const_define import *

def getHistory(userID, historyDir = HISTORY_DIR):
    path = os.path.join(historyDir, f"{userID}.json")

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []

def saveHistory(userID, history, historyDir = HISTORY_DIR):
    os.makedirs(        # 自动创建目录
        historyDir,
        exist_ok=True,
    )

    path = os.path.join(historyDir, f"{userID}.json")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)
