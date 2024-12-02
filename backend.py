from dataclasses import dataclass
from fastapi import FastAPI, Request
import requests
from db.sqlite_connection import Database
from aiogram import Bot
from config import load_config
import uvicorn

config = load_config("config.json", "texts.yml")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
db = Database(config.tg_bot.db_name)

app = FastAPI(
    title="vk_sync_bot",
    summary="",
    version="0.0.1",
    description="Your AI assistant",
)


@dataclass
class hub:
    mode: str
    challenge: str | int
    verify_token: str | int


@app.post("/instagram/", name="Wellcome")
async def user(request: Request):
    res = request.query_params.get('hub.challenge')
    print(request.body())
    return


@app.get("/instagram/", name="Wellcome")
async def user(request: Request):
    res = request.query_params.get('hub.challenge')
    print(request.body())
    return int(res)


@app.get("/vkCallback", name="Wellcome")
async def user(code: str, state: str):

    code = code
    response = requests.get(
        f'https://oauth.vk.com/access_token?client_id=51753414&client_secret={config.tg_bot.client_secret}&redirect_uri={config.tg_bot.redirect_uri}&code={code}')
    print(response.json())

    db.update_access_token(state, response.json()["access_token"])
    await bot.send_message(state, "Успешно...")
    return {"message": "Success"}


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
