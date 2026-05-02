from urllib import response

from fastapi import FastAPI
from openai.resources.chat.completions import messages
from pydantic import BaseModel
from openai import OpenAI
import os
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

client = OpenAI(
    api_key=os.getenv('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

chat_history = [
    {
        "role": "system",
        "content": "你是一个专业电商客服助手，负责回答用户关于商品、退款、物流的问题。"
    }
]


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(rep: ChatRequest):
    global chat_history
    chat_history.append({
        "role": "user",
        "content": rep.message
    })

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=chat_history
    )

    answer = response.choices[0].message.content

    chat_history.append({
        "role": "assistant",
        "content": answer
    })

    return {
        "answer": answer
    }

@app.post("/clear")
def clear():
    global chat_history
    chat_history = [
        {
            "role": "system",
            "content": "你是一个专业电商客服助手，负责回答用户关于商品、退款、物流的问题。"
        }
    ]
    return {"message","消息已清空！"}
