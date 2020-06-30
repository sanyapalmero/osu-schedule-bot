import json
import logging

import requests
from telegram.bot import Bot
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from telegram.utils.request import Request

import settings
from database import Database

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(bot, context):
    """/start command"""
    message = "Привет! Я - Хлоя, и я буду присылать тебе твое расписание.\nПришли мне, пожалуйста, в следующем сообщении ссылку на твоё расписание.\nВажно, чтобы расписание было на весь семестр, а не на две недели."
    bot.send_message(chat_id=context.message.chat_id, text=message)


def message_handle(bot, context):
    user_id = context.message.chat_id
    schedule = context.message.text
    database = Database(settings.DATABASE_FILE)
    user_exists = database.user_exists(user_id)
    if not user_exists:
        mask = "https://www.osu.ru/pages/schedule/"
        if schedule.startswith(mask):
            database.subscribe_user(user_id, schedule)
            message = f"Спасибо! Твое расписание: {schedule} было успешно сохранено.\nС завтрашнего дня в 7:00 каждый день ты будешь получать свое расписание! :)"
            bot.send_message(chat_id=user_id, text=message)
        else:
            bot.send_message(chat_id=user_id, text="Ой, кажется это не ссылка на расписание :(")
    else:
        bot.send_message(chat_id=user_id, text="Ой, а ты уже подписан, хочешь обновить ссылку на расписание? Введи /update")


def main():
    print("---Bot started---")
    bot = Bot(settings.BOT_TOKEN)
    print("---Connected---")

    updater = Updater(bot=bot)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    message_handler = MessageHandler(Filters.text, message_handle)
    dispatcher.add_handler(message_handler)

    updater.start_polling()


main()
