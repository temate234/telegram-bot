import os
import telebot
from telebot import types

TELEGRAM_API_TOKEN = '6895670985:AAGjbht0bNbA_HkqBL2GXKyBg2qudquGg3Y'
bot = telebot.TeleBot(TELEGRAM_API_TOKEN)

# Словарь для соответствия русских и английских названий дней недели
day_mapping = {
    '/понедельник': '/monday',
    '/вторник': '/tuesday',
    '/среда': '/wednesday',
    '/четверг': '/thursday',
    '/пятница': '/friday',
    '/суббота': '/saturday',
    '/воскресенье': '/sunday'
}

def normalize_command(command):
    return day_mapping.get(command.lower(), None)

@bot.message_handler(commands=['start'])
def handle_start(message):
    try:
        markup = types.ReplyKeyboardMarkup(row_width=2)
        days = ["/понедельник", "/вторник", "/среда", "/четверг", "/пятница", "/суббота", "/воскресенье"]
        buttons = [types.KeyboardButton(day) for day in days]
        markup.add(*buttons)

        bot.reply_to(message, 'Привет! Я бот с расписанием.', reply_markup=markup)
    except Exception as e:
        print(f"Error in handle_start: {e}")

@bot.message_handler(func=lambda message: normalize_command(message.text) is not None)
def handle_schedule(message):
    try:
        day = normalize_command(message.text)  # возвращаем английское название дня
        filename = f"META/{day}.txt"

        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                schedule_text = file.read()

            # Исключаем строку с названием дня из ответа бота
            schedule_text = schedule_text.replace(f"{day.capitalize()}:", "")

            bot.reply_to(message, f"Расписание:\n\n{schedule_text.strip()}")
        else:
            bot.reply_to(message, f"Еблан, дома сиди")
    except Exception as e:
        print(f"Error in handle_schedule: {e}")

@bot.message_handler(func=lambda message: True)  # обработка всех остальных сообщений
def handle_unknown(message):
    try:
        bot.reply_to(message, "Неверная команда")
    except Exception as e:
        print(f"Error in handle_unknown: {e}")

if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Error in polling: {e}")
