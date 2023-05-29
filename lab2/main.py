import random
import telebot
from telebot import types

TOKEN = '6097636425:AAHnu2-qLRRL_BZ1sOo24jlqQKqTUsX4okQ'

bot = telebot.TeleBot(TOKEN)

questions = [
    {
        'index': 1,
        'question': 'Кто был первым императором России?',
        'answers': ['Иван Грозный', 'Петр I', 'Александр I', 'Николай II'],
        'correct_answer': 1
    },
    {
        'index': 2,
        'question': 'Когда произошла Октябрьская революция в России?',
        'answers': ['1917 год', '1905 год', '1921 год', '1914 год'],
        'correct_answer': 0
    },
    {
        'index': 3,
        'question': 'Кто был последним царем России?',
        'answers': ['Александр III', 'Николай II', 'Александр II', 'Петр II'],
        'correct_answer': 1
    },
    {
        'index': 4,
        'question': 'Какая территория стала причиной Крымской войны 1853-1856 гг.?',
        'answers': ['Украина', 'Казахстан', 'Крым', 'Польша'],
        'correct_answer': 2
    },
    {
        'index': 5,
        'question': 'Какой год считается началом Первой мировой войны для России?',
        'answers': ['1914 год', '1917 год', '1918 год', '1919 год'],
        'correct_answer': 0
    }
]

def generate_markup(question): # Генерация клавиатуры с вариантами ответов
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    answers = question['answers']
    for answer in answers:
        markup.add(types.KeyboardButton(answer))
    return markup

@bot.message_handler(commands=['start'])
def start(message): # Приветственное сообщение и кнопка Начать игру
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton('Начать игру')
    markup.add(item)
    bot.send_message(message.chat.id, 'Добро пожаловать в игру "Кто хочет стать миллионером"!\nНажмите кнопку "Начать игру", чтобы начать.', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Начать игру')
def play_game(message): # Начало игры - задается первый вопрос
    ask_question(message.chat.id, 1, 0)

def ask_question(chat_id, question_index, correct_count):
    question = next((q for q in questions if q['index'] == question_index), None)
    if question:
        markup = generate_markup(question)
        bot.send_message(chat_id, f'Вопрос {question["index"]}: {question["question"]}', reply_markup=markup)  # Отправка вопроса с вариантами ответов
        bot.register_next_step_handler_by_chat_id(chat_id, check_answer, question, correct_count)
    else:
        stop_game(chat_id, correct_count) # Игра завершена - выводится результат

def check_answer(message, question, correct_count):
    user_answer = message.text
    correct_answer = question['answers'][question['correct_answer']]
    if user_answer == correct_answer:
        bot.send_message(message.chat.id, 'Правильно! Вы ответили верно.К вашему баллансу прибавляется - 200 000 рублей!!') # Ответ правильный
        next_question_index = question['index'] + 1
        next_correct_count = correct_count + 1
        if next_correct_count == 5:
            stop_game(message.chat.id, next_correct_count) # Игра завершена - все вопросы правильно
        else:
            ask_question(message.chat.id, next_question_index, next_correct_count) # Переход к следующему вопросу
    else:
        bot.send_message(message.chat.id, f'К сожалению, вы ответили неправильно. Правильный ответ: {correct_answer}')  # Ответ неправильный
        stop_game(message.chat.id, correct_count)

def stop_game(chat_id, correct_count):
    if correct_count == 5:
        bot.send_message(chat_id, 'Поздравляю! Вы ответили на все вопросы. Вы стали миллионером, введите все данные своей карточки(с обратной стороны тоже) и мы отправим вам ваш выйгрыш!!!!') # Игра завершена - все вопросы правильно
    else:
        bot.send_message(chat_id, 'Игра завершена.') # Игра завершена - не все вопросы правильно
    restart_game(chat_id)

def restart_game(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)   # Возможность начать игру заново
    item = types.KeyboardButton('Начать игру')
    markup.add(item)
    bot.send_message(chat_id, 'Нажмите кнопку "Начать игру", чтобы начать заново.', reply_markup=markup)

bot.polling()