from gradio import *
from const_define import *

def replyGeneration(
        tokenizer, 
        model, 
        inputs,
        TextIteratorStreamer,
        threading
    ):

    streamer = TextIteratorStreamer(
        tokenizer,
        skip_prompt=True,
        skip_special_tokens=True,
    )

    generation_kwargs = dict(
        **inputs,
        streamer=streamer,
        max_new_tokens=MAX_NEW_TOKENS,
        temperature=TEMPERATURE,
        top_p=TOP_P,
        repetition_penalty=REPETITION_PENALTY,
        do_sample=True,
    )

    thread = threading.Thread(
        target=model.generate,
        kwargs=generation_kwargs,
    )

    thread.start()


    answer = ""

    for new_text in streamer:
        answer += new_text
        yield answer   # 返回历史对话