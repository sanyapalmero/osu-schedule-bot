import requests
import logging
import settings
import json

from telegram.bot import Bot
from telegram.utils.request import Request
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


# TODO:
# 1 - сохранение chat_id и расписания в json
# 2 - рассылка расписания в указанное время
# 3 - метод удаления пользователя из рассылки


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(bot, context):
    """/start command"""
    message = "Привет! Я - Хлоя, и я буду присылать тебе твое расписание.\nПришли мне, пожалуйста, в следующем сообщении ссылку на твоё расписание.\nВажно, чтобы расписание было на весь семестр, а не на две недели."
    bot.send_message(chat_id=context.message.chat_id, text=message)


def message_handle(bot, context):
    mask = "https://www.osu.ru/pages/schedule/"
    if context.message.text.startswith(mask):
        message = f"Спасибо! Твое расписание: {context.message.text} было успешно сохранено.\nС завтрашнего дня в 7:00 каждый день ты будешь получать свое расписание! :)"
        bot.send_message(chat_id=context.message.chat_id, text=message)
    else:
        bot.send_message(chat_id=context.message.chat_id, text="Ой, кажется это не ссылка на расписание :(")


class User:
    def __init__(self, user_chat_id, user_schedule):
        self.user_chat_id = user_chat_id
        self.user_schedule = user_schedule


def open_storage():
    with open(settings.STORAGE_FILE, "r") as file:
        data = json.load(file)
        return data


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
