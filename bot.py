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


SCHEDULE_MASK = "osu.ru/pages/schedule/"


def help(bot, context):
    """/help command"""
    message = "Тебе доступные следующие команды:\n/start - Добавить расписание\n/delete Отписаться от рассылки\n/help Помощь\n По всем вопросам: @pa1m3r0"
    bot.send_message(chat_id=context.message.chat_id, text=message)


def start(bot, context):
    """/start command"""
    message = "Привет! Я - Хлоя, и я буду присылать тебе твое расписание.\nПришли мне, пожалуйста, в следующем сообщении ссылку на твоё расписание.\nВажно, чтобы расписание было на весь семестр, а не на две недели.\nТакже ты можешь ввести /help и посмотреть все доступные команды"
    bot.send_message(chat_id=context.message.chat_id, text=message)


def delete(bot, context):
    """/delete command"""
    user_id = context.message.chat_id
    database = Database(settings.DATABASE_FILE)
    user_exists = database.user_exists(user_id)
    user_is_active = database.is_active_user(user_id)

    if user_exists and user_is_active:
        active = database.is_active_user(user_id)
        database.unsubscribe_user(user_id)
        message = "Готово! Ты больше не будешь получать своё расписание. Надеюсь, ты ещё вернёшься :)"
        bot.send_message(chat_id=user_id, text=message)
    else:
        message = "Ой, кажется у меня и так нет твоего расписания, может быть, ты хочешь добавить его? Введи /help чтобы узнать все мои команды."
        bot.send_message(chat_id=user_id, text=message)


def message_handle(bot, context):
    user_id = context.message.chat_id
    schedule = context.message.text
    database = Database(settings.DATABASE_FILE)
    user_exists = database.user_exists(user_id)

    if SCHEDULE_MASK not in schedule:
        bot.send_message(chat_id=user_id, text="Ой, кажется это не ссылка на расписание :(")
        return

    if user_exists:
        database.update_schedule(user_id, schedule)
    else:
        database.subscribe_user(user_id, schedule)

    message = f"Спасибо! Твое расписание: {schedule} было успешно сохранено.\nС завтрашнего дня в 7:00 каждый день ты будешь получать свое расписание! :)"
    bot.send_message(chat_id=user_id, text=message)


def main():
    print("---Bot started---")
    bot = Bot(settings.BOT_TOKEN)
    print("---Connected---")

    updater = Updater(bot=bot)
    dispatcher = updater.dispatcher

    help_handler = CommandHandler('help', help)
    dispatcher.add_handler(help_handler)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    delete_handler = CommandHandler('delete', delete)
    dispatcher.add_handler(delete_handler)

    message_handler = MessageHandler(Filters.text, message_handle)
    dispatcher.add_handler(message_handler)

    updater.start_polling()

    updater.idle()

main()
