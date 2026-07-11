import gradio as gr

def createUI(chatFunction, mic_chatFunction):

    with gr.Blocks(
        title = "绪山真寻 | 你的 AI 助手",
        theme = gr.themes.Soft()
    ) as GUI:
        gr.Markdown("# 绪山真寻 AI")
        gr.Markdown("## 可以本地离线部署，基于《别当欧尼酱了》的主角绪山真寻的AI助手，由Qwen2.5-1.5B-Instruct模型驱动。")

        chatbot = gr.Chatbot(height = 600)

        with gr.Row():

            audio = gr.Audio(
                sources = ["microphone"],
                type = "filepath",
                scale = 1
            )

            textbox = gr.Textbox(
                placeholder = "输入消息……",
                scale = 8,
                show_label = False
            )

            send = gr.Button(
                "发送",
                scale = 1
            )

        with gr.Row():
            clear = gr.Button("🗑 清空聊天")
            regenerate = gr.Button("🔄 重试")

        send.click(
            fn=chatFunction,
            inputs=[textbox, chatbot],
            outputs=chatbot
        ).then(
            lambda: "",
            outputs=textbox
        )

        textbox.submit(
            fn=chatFunction,
            inputs=[textbox, chatbot],
            outputs=chatbot
        ).then(
            lambda: "",
            outputs=textbox
        )

        audio.stop_recording(
            fn=mic_chatFunction,
            inputs=[audio, chatbot],
            outputs=chatbot
        )

        clear.click(
            lambda: [],
            outputs=chatbot
        )

    return GUI