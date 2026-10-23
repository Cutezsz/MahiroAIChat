from const_define import (
    SEARCH_MAX_RESULTS, SEARCH_BODY_MAX_LEN, SEARCH_TIMEOUT
)

import os
from openai import OpenAI
from tavily import TavilyClient


deepseek_client = OpenAI(
    api_key = os.environ["DEEPSEEK_API_KEY"],
    base_url = "https://api.deepseek.com/"
)

def webSearch(query, max_results = SEARCH_MAX_RESULTS):    # 最大返回结果
    try:
        api_key = os.environ["TAVILY_API_KEY"]
        client = TavilyClient(api_key=api_key)

        response = client.search(
            query = query, 
            max_results = max_results, 
            search_depth = "basic",     # 太烧钱了
            timeout = SEARCH_TIMEOUT, 
            language = "zh-cn"
        )
        results = response.get("results", [])
        if not results:
            return "没有找到相关结果"
        
        lines = []
        for res in results:
            title = res.get("title", "无标题")
            body = (res.get("content") or "")[:SEARCH_BODY_MAX_LEN].replace("\n", " ")
            lines.append(f"- {title}: {body}")
        return "\n".join(lines)     # 以 \n 为分隔符
    
    except Exception as e:
        print(e)
        return f"搜索暂时不可用：{e}"


def think(question):    # question表示“模型认为自己需要想什么”
    try:
        response = deepseek_client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[
                {"role": "system", "content": "给出简短的结论，不要罗列‘适合/不适合/建议/结论’这类结构。对于数学问题可以详细一点。"},
                {"role": "user", "content": question},],
            extra_body={"thinking": {"type": "enabled"}},    # 返回针对模型传进去的那个问题，生成的一段结论性文本
        )
        return response.choices[0].message.content or "（没想出来）"
    
    except Exception as e:
        print(f"[think] {e}")
        return f"思考暂时不可用：{e}"



TOOLS = [   # 模型可用的所有工具
    {
        "type": "function",
        "function": {
            "name": "webSearch",
            "description": "搜索网页。用户问到近期新闻、实时信息，或你确实不知道的事情时必须调用。查询词要简洁。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词，例如：2026年10月新番",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "think",
            "description": "当问题需要多步推理、分析比较、权衡利弊，或你需要先理清思路再回答时调用。简单寒暄、事实查询、闲聊不要调用。传入你想想清楚的问题。",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string", 
                        "description": 
                            """需要深入思考的核心问题。用一两句话写清楚要权衡或推理什么，并带上做出判断所需的背景（例如用户的偏好、限制条件、已讨论过的选项）。
                            不要原样复制用户的话，也不要复述整段对话。问题中不要包含对输出格式的要求，输出约束由 think 工具自身处理。"""
                    }
                },
                "required": ["question"],
            },
        },
    },
]

TOOL_FUNCTIONS = {
    "webSearch": webSearch,
    "think": think,
}

def execute(name, arguments):   # name为要调用的工具，arguments是参数
    func = TOOL_FUNCTIONS.get(name)
    if func is None:
        return f"未知工具: {name}"
    try:
        return func(**arguments)
    except TypeError as e:
        return f"工具参数错误: {e}"
    except Exception as e:
        return f"工具执行失败: {e}"