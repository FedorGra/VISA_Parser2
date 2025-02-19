import logging
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode

TOKEN = "8109609226:AAHX--3jzj4CFkofimecqHSZ8S0Qvuaa3SA"
CHAT_ID = "189920809"
URL = "https://it.tlscontact.com/by/msq/page.php?pid=news&l=ru"
CHECK_INTERVAL = 300  # Проверять раз в 5 минут

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
latest_news = ""

async def fetch_news():
    global latest_news
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                news_section = soup.find("div", class_="content-container")
                if news_section:
                    news_text = news_section.get_text(strip=True)
                    if news_text != latest_news:
                        latest_news = news_text
                        await bot.send_message(CHAT_ID, f"📰 Новость обновлена: {news_text}")
            else:
                logging.warning("Не удалось получить данные со страницы")

async def scheduled_checker():
    while True:
        await fetch_news()
        await asyncio.sleep(CHECK_INTERVAL)

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет! Я бот для мониторинга новостей визового центра. Я сообщу тебе, когда появятся обновления.")

async def main():
    asyncio.create_task(scheduled_checker())
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
