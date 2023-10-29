from fastapi import FastAPI
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


@app.get("/vkCallback", name="Wellcome")
async def user(code: str, state: str):

    code = code
    response = requests.get(
        f'https://oauth.vk.com/access_token?client_id=51753414&client_secret={config.tg_bot.client_secret}&redirect_uri={config.tg_bot.redirect_uri}&code={code}')
    print(response.json()["access_token"])

    db.update_access_token(state, response.json()["access_token"])
    await bot.send_message(state, "Успешно...")
    return {"message": "Success"}


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
