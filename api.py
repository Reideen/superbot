# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request
app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}

# Задаем параметры приложения Flask.
@app.route("/", methods=['POST','GET'])

def main():
    # Функция получает тело запроса и возвращает ответ.
    # Настройки
    from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
    import apiai, json

    updater = Updater(token='350756715:AAHdbRURFAyWJ6K_hLkS30wNDs5V9z6iUic')  # Токен API к Telegram
    dispatcher = updater.dispatcher


    # Обработка команд
    def startCommand(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?')


    def textMessage(bot, update):
        request = apiai.ApiAI('fbbeb98758a2488789b601b9e76b85ac').text_request()  # Токен API к Dialogflow
        request.lang = 'ru'  # На каком языке будет послан запрос
        request.session_id = 'superbotinok'  # ID Сессии диалога (нужно, чтобы потом учить бота)
        request.query = update.message.text  # Посылаем запрос к ИИ с сообщением от юзера
        responseJson = json.loads(request.getresponse().read().decode('utf-8'))
        response = responseJson['result']['fulfillment']['speech']  # Разбираем JSON и вытаскиваем ответ
        # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
        if response:
            bot.send_message(chat_id=update.message.chat_id, text=response)
        else:
            bot.send_message(chat_id=update.message.chat_id, text='Пожалуйста подождите, скоро мы ответим на ваш вопрос!')


    # Хендлеры
    start_command_handler = CommandHandler('start', startCommand)
    text_message_handler = MessageHandler(Filters.text, textMessage)
    # Добавляем хендлеры в диспетчер
    dispatcher.add_handler(start_command_handler)
    dispatcher.add_handler(text_message_handler)
    # Начинаем поиск обновлений
    updater.start_polling(clean=True)
    # Останавливаем бота, если были нажаты Ctrl + C
    updater.idle()