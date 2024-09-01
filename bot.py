import g4f
import telebot
import random

# Инициализация бота
bot = telebot.TeleBot("7507865569:AAFJmRCCdZL0hn0dH-1YfoOpgpYoVpVcuwQ")

def is_chinese(text):
    # Проверка, содержит ли текст китайские символы
    return any('\u4e00' <= char <= '\u9fff' for char in text)

def get_response(text):
    try:
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Используем модель GPT-3.5-turbo
            messages=[{"role": "user", "content": text}],
            stream=False,
        )
        return response
    except Exception as e:
        return f"Ошибка при запросе: {e}"

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Отправьте мне любой текст, и я на него отвечу.")

@bot.message_handler(func=lambda message: True)  # Обработчик для всех текстовых сообщений
def handle_text(message):
    text = message.text
    bot.send_message(message.chat.id, "Пожалуйста подождите")

    def process_response(response):
        if isinstance(response, str) and is_chinese(response):
            bot.delete_message(message.chat.id, message.message_id)  # Удаление сообщения
            response = get_response(text)  # Пересоздание запроса
        return response

    # Получение и обработка ответа
    try:
        response = get_response(text)
        response = process_response(response)
        if isinstance(response, str):
            try:
                bot.reply_to(message, response)
            except telebot.apihelper.ApiTelegramException as e:
                # Логирование и обработка ошибки
                bot.send_message(message.chat.id, f"Произошла ошибка при ответе: {e}")
        else:
            bot.send_message(message.chat.id, "Получен неожиданный формат ответа.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")

bot.polling()
