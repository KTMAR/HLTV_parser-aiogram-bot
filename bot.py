import json
from aiogram import Bot, executor, Dispatcher, types
from config import token
from aiogram.utils.markdown import hlink
from main import check_news_update
from aiogram.dispatcher.filters import Text

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Все новости', 'Последние 8', 'Свежие']

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Новости HLTV', reply_markup=keyboard)


@dp.message_handler(Text(equals='Все новости'))
async def get_all_news(message: types.Message):
    with open('news_dict.json') as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items()):
        news = f'<b>{v["article_date"]}</b>\n' \
               f'{hlink(v["article_title"], v["article_url"])}\n' \

        await message.answer(news)


@dp.message_handler(Text(equals='Последние 8'))
async def get_last_five_news(message: types.Message):

    with open('news_dict.json') as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[-8:]:
        news = f'<b>{v["article_date"]}</b>\n' \
               f'{hlink(v["article_title"], v["article_url"])}\n' \

        await message.answer(news)


@dp.message_handler(Text(equals='Свежие'))
async def get_fresh_news(message: types.Message):
    fresh_news = check_news_update()

    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items())[-8:]:
            news = f'<b>{v["article_date"]}</b>\n' \
                   f'{hlink(v["article_title"], v["article_url"])}\n' \

            await message.answer(news)
    else:
        await message.answer('Пока ничего нового на HLTV')


if __name__ == '__main__':
    executor.start_polling(dp)
