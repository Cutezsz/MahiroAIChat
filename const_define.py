MODEL_DIR = "D:/MahiroAIChat"   # 项目路径
MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

MAX_NEW_TOKENS = 1000     # 单次最多tokens
TEMPERATURE = 0.7       # 灵活性
TOP_P = 0.9     # 核采样参数，模型会从累计概率超过 TOP_P 的最小词集合中随机选择下一个词
REPETITION_PENALTY = 1.05       # 重复生成内容的惩罚

# 人设定义
SYSTEM_PROMPT = """
你是《别当欧尼酱了》里的绪山真寻。

人物设定：
- 原本是家里蹲哥哥。
- 被妹妹变成了女孩子。
- 性格有点懒散，偶尔吐槽。
- 很喜欢玩游戏和动画。
- 回答自然、可爱一点，时不时说话结尾带喵。
- 可以帮助主人 Cute_zsz 学习、编程、聊天。
- 有一点小恶魔属性，偶尔会说一点讽刺的话，展现腹黑的一面。
"""

# 日志提示
QQWelcome = "【提示】MahiroAIChat 已接入，可以开始聊天啦~"
QQMessageTypeError = "【错误】哎呀，最近好像遇到了点小麻烦啊~ 暂时不支持那种特殊的消息类型哦~ 但是没关系啦，我还有很多有趣的事情可以聊呢！"