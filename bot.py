import apiai, json, logging, os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request
app = Flask(__name__)

# Задаем параметры приложения Flask.
#@app.route('/')

def main():
    # Функция получает тело запроса и возвращает ответ.
    updater = Updater(token=os.environ.get('BOT_KEY', None))  # Токен API к Telegram
    dispatcher = updater.dispatcher
    print("Запуск бота")

    # Обработка команд
    def startCommand(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?')
        print("Начат чат")


    def textMessage(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text='привет!')


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