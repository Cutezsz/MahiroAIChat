from pathlib import Path

MODEL_DIR = "D:/MahiroAIChat"   # 项目路径
MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

# 模型参数
MAX_NEW_TOKENS = 8192     # 单次最多tokens
TEMPERATURE = 0.7       # 灵活性
TOP_P = 0.9     # 核采样参数，模型会从累计概率超过 TOP_P 的最小词集合中随机选择下一个词
REPETITION_PENALTY = 1.15       # 重复生成内容的惩罚

# 关于聊天
MAX_HISTORY = 20    # 最大聊天记录条数（记忆限制）
MAX_GROUP_HISTORY = 50

SELF_QQ_ID = "3453211161"

HISTORY_DIR = "qq_history" 
GROUP_HISTORY_DIR = "qq_history/group"

ACTIVE_CONTENT_LEN = 10    # 判断是否主动对话依据的上下文长度
ACTIVE_CHAT_THRESHOLD = 0.45   # 活跃聊天阈值
ACTIVE_CHAT_THRESHOLD_EXTRA = 0.8   # 如果权重超过这个数，可以无视冷却
ACTIVE_COLDDOWN = 20   # 主动对话冷却时间

# 人设定义
PERSONA = "PERSONA/mahiro.md"       # 人设
SYSTEM_PROMPT = Path(PERSONA).read_text(encoding="utf-8")

# 提示 警告 报错
QQWelcome = "真寻真寻来了哦！"
QQMessageTypeError = "Unsupported Message Type"
REPLY_EXCEEDED = "Reply Exceeded"
UNKNOWN_ERROR = "Unknown Error"
TOOL_FALLBACK_REPLY = "Tool Fallback"

# TOOLS
MAX_TOOL_ROUNDS = 5     # 最多使用多少次tools

SEARCH_ENGINE = "https://cn.bing.com/search"   # 搜索引擎
SEARCH_MAX_RESULTS = 3   # 搜索结果条数
SEARCH_BODY_MAX_LEN = 200   # 搜索结果正文最大长度
SEARCH_TIMEOUT = 10   # 搜索超时时间