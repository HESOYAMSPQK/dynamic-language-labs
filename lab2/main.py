import random
import telebot
from telebot import types

TOKEN = '6097636425:AAHnu2-qLRRL_BZ1sOo24jlqQKqTUsX4okQ'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_game(message):
    # Отправляем приветственное сообщение
    bot.reply_to(message, "Привет! Я загадал число от 1 до 100. Попробуй угадать!")

    # Отправляем картинку
    with open('image.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)

    # Создаем кнопку "Начать игру"
    start_button = types.KeyboardButton("Начать игру")
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(start_button)

    # Отправляем клавиатуру с кнопкой
    bot.send_message(message.chat.id, "Нажми на кнопку, чтобы начать игру.", reply_markup=keyboard)

    # Загадываем число
    bot.current_game_number = random.randint(1, 100)

@bot.message_handler(func=lambda message: message.text == "Начать игру")
def guess_number(message):
    # Создаем кнопки "Это число простое?" и "Это число четное?"
    prime_button = types.KeyboardButton("Это число простое?")
    even_button = types.KeyboardButton("Это число четное?")
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(prime_button, even_button)

    # Отправляем клавиатуру с кнопками
    bot.send_message(message.chat.id, "Выбери вопрос:", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "Это число простое?")
def check_prime(message):
    number = bot.current_game_number
    is_prime = True

    # Проверяем, является ли число простым
    if number < 2:
        is_prime = False
    else:
        for i in range(2, int(number ** 0.5) + 1):
            if number % i == 0:
                is_prime = False
                break

    # Отправляем ответ
    if is_prime:
        bot.reply_to(message, "Да, загаданное число простое!")
    else:
        bot.reply_to(message, "Нет, загаданное число не простое.")

@bot.message_handler(func=lambda message: message.text == "Это число четное?")
def check_even(message):
    number = bot.current_game_number

    # Проверяем, является ли число четным
    if number % 2 == 0:
        bot.reply_to(message, "Да, загаданное число четное!")
    else:
        bot.reply_to(message, "Нет, загаданное число не четное.")

@bot.message_handler(func=lambda message: True)
def process_guess(message):
    try:
        # Получаем введенное пользователем число
        user_number = int(message.text)

        # Сравниваем с загаданным числом
        if user_number < bot.current_game_number:
            bot.reply_to(message, "Загаданное число больше!")
        elif user_number > bot.current_game_number:
            bot.reply_to(message, "Загаданное число меньше!")
        else:
            bot.reply_to(message, "Поздравляю, ты угадал число!")
            bot.current_game_number = None

    except ValueError:
        bot.reply_to(message, "Пожалуйста, введите целое число.")

if __name__ == '__main__':
    bot.polling()