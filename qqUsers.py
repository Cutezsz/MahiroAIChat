import json
import os
import time

FILE = "qq_users.json"

def getQQUsers():
    if not os.path.exists(FILE):
        return []

    try:
        with open(FILE, "r", encoding="utf-8") as f:
            users = json.load(f)
        
        if isinstance(users, list):
            return users
        
        if isinstance(users, dict):     # 如果是字典就加一个列表
            return [users]
    except:
        return []
    
def saveUsers(user):    # 给定用户数据，进行覆写
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(user, f, ensure_ascii=False, indent=4)

def addUser(id, name):
    users = getQQUsers()
    
    for user in users:
        if user["id"] == id:
            user["name"] = name
            user["chat_count"] += 1
            user["last_chat_time"] = time.time()
            saveUsers(users)
            return
        
    users.append({"id": id, "name": name, "last_chat_time": time.time(), "chat_count": 1})  # 不存在就自动创建
    saveUsers(users)