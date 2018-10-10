import apiai, json, logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request
app = Flask(__name__)

# Задаем параметры приложения Flask.
#@app.route('/')

def main():
    # Функция получает тело запроса и возвращает ответ.
    updater = Updater(token='486690728:AAHJJfmnn5yzSAQeiv5OzBW3p4FA9ytsJ0Y')  # Токен API к Telegram
    dispatcher = updater.dispatcher
    print("Запуск бота")

    # Обработка команд
    def startCommand(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?')
        print("Начат чат")


    def textMessage(bot, update):
        request = apiai.ApiAI('ecc6943654264bd4b60e788154e1a016').text_request()  # Токен API к Dialogflow
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
    print("Хэндлеры добавлены")
    return updater.start_polling(clean=True)

main()
app.run()