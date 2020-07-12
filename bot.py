import json
import logging
from datetime import time

import requests
from telegram import Update
from telegram.bot import Bot
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)
from telegram.utils.request import Request

import settings
from database import Database
from schedule import get_user_schedule

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


SCHEDULE_MASK = "osu.ru/pages/schedule/"


def help(update: Update, context: CallbackContext):
    """/help command"""
    message = "Тебе доступные следующие команды:\n/start - Добавить расписание\n/delete Отписаться от рассылки\n/help Помощь\n По всем вопросам: @pa1m3r0"
    context.bot.send_message(chat_id=update.message.chat_id, text=message)


def start(update: Update, context: CallbackContext):
    """/start command"""
    message = "Привет! Я - Хлоя, и я буду присылать тебе твое расписание.\nПришли мне, пожалуйста, в следующем сообщении ссылку на твоё расписание.\nВажно, чтобы расписание было на весь семестр, а не на две недели.\nТакже ты можешь ввести /help и посмотреть все доступные команды"
    context.bot.send_message(chat_id=update.message.chat_id, text=message)


def delete(update: Update, context: CallbackContext):
    """/delete command"""
    user_id = update.message.chat_id
    database = Database(settings.DATABASE_FILE)
    user_exists = database.user_exists(user_id)
    user_is_active = database.is_active_user(user_id)

    if user_exists and user_is_active:
        active = database.is_active_user(user_id)
        database.unsubscribe_user(user_id)
        message = "Готово! Ты больше не будешь получать своё расписание. Надеюсь, ты ещё вернёшься :)"
        context.bot.send_message(chat_id=user_id, text=message)
    else:
        message = "Ой, кажется у меня и так нет твоего расписания, может быть, ты хочешь добавить его? Введи /help чтобы узнать все мои команды."
        context.bot.send_message(chat_id=user_id, text=message)


def message_handle(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    schedule = update.message.text
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
    context.bot.send_message(chat_id=user_id, text=message)


def send_schedule_task(context: CallbackContext):
    database = Database(settings.DATABASE_FILE)
    active_users = database.get_active_users()
    for user in active_users:
        user_id = user[0]
        schedule_link = user[1]
        schedule = get_user_schedule(schedule_link)
        context.bot.send_message(chat_id=user_id, text=schedule)


def main():
    print("---Bot started---")
    bot = Bot(settings.BOT_TOKEN)
    print("---Connected---")

    updater = Updater(bot=bot, use_context=True)
    dispatcher = updater.dispatcher

    help_handler = CommandHandler('help', help)
    dispatcher.add_handler(help_handler)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    delete_handler = CommandHandler('delete', delete)
    dispatcher.add_handler(delete_handler)

    message_handler = MessageHandler(Filters.text, message_handle)
    dispatcher.add_handler(message_handler)

    updater.job_queue.run_daily(send_schedule_task, time=time(7, 0, 0))

    updater.start_polling()

    updater.idle()

main()
