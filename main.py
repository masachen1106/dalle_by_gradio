import os
import sys

import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

openai_key = os.getenv("OPENAI_KEY")

if openai_key == "<YOUR_OPENAI_KEY>":
    openai_key = ""

if openai_key == "":
    sys.exit("Please Provide Your OpenAI API Key")


def generate_image(text):
    model = "dall-e-3"
    quality = "standard"
    size = "1024x1024"
    print('input: ', text)
    try:
        client = OpenAI(api_key=openai_key)

        response = client.images.generate(
            prompt=text,
            model=model,
            quality=quality,
            size=size,
            n=1,
        )
    except Exception as error:
        print(str(error))
        raise gr.Error("An error occurred while generating.")

    return response.data[0].url


with gr.Blocks() as demo:
    gr.Markdown("# <center> AI 夢工廠 </center>")
    
    text = gr.Textbox(label="Input Text",
                      placeholder="輸入文字並點擊 \"開始\" 按鈕" )
    btn = gr.Button("開始")
    output_image = gr.Image(label="Image Output")

    text.submit(fn=generate_image, inputs=text, outputs=output_image, api_name="generate_image")
    btn.click(fn=generate_image, inputs=text, outputs=output_image, api_name=False)
demo.queue(default_concurrency_limit=16)
demo.launch(share=True)
