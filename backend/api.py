from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from summary import summarizer
from pydantic import BaseModel
bot =  summarizer()

app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Input(BaseModel):
    paragraph :str

@app.post("/summarize")
async def sum(input : Input):
    ans = bot.summarize(input.paragraph)
    return {"answer": ans}