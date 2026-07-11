MODEL_DIR = "D:/MahiroAIChat"   # 项目路径

MAX_NEW_TOKENS = 1000     # 单次最多tokens
TEMPERATURE = 0.7       # 灵活性
TOP_P = 0.9     # 核采样参数，模型会从累计概率超过 TOP_P 的最小词集合中随机选择下一个词
REPETITION_PENALTY = 1.05       # 重复生成内容的惩罚
