import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties

API_TOKEN = "8157173233:AAHtK_IXMmXOmK8M6NlUr5n-gFBRoRV8ZdQ"

# Уроки
lessons = {
    1: "\U0001F4D8 Урок 1: Приветствие\n\n"
       "\U0001F539 Hello! — Привет!\n"
       "\U0001F539 How are you? — Как дела?\n"
       "\U0001F539 I’m fine, thank you. — Я в порядке, спасибо.\n"
       "\U0001F539 My name is... — Меня зовут...\n"
       "\U0001F539 Nice to meet you! — Приятно познакомиться!",
    2: "\U0001F4D8 Урок 2: Вопросы\n\n"
       "\U0001F539 What? — Что?\n"
       "\U0001F539 Who? — Кто?\n"
       "\U0001F539 Where? — Где?\n"
       "\U0001F539 How much? — Сколько?\n"
       "\U0001F539 Why? — Почему?",
    3: "\U0001F4D8 Урок 3: Еда и напитки\n\n"
       "\U0001F539 I like coffee. — Мне нравится кофе.\n"
       "\U0001F539 I’m hungry. — Я голоден.\n"
       "\U0001F539 I want pizza. — Я хочу пиццу.\n"
       "\U0001F539 Water, please. — Воды, пожалуйста.",
    4: "\U0001F4D8 Урок 4: В магазине\n\n"
       "\U0001F539 How much is it? — Сколько это стоит?\n"
       "\U0001F539 I want to buy this. — Я хочу это купить.\n"
       "\U0001F539 Do you have this in black? — Есть это в чёрном?",
    5: "\U0001F4D8 Урок 5: Время и дни\n\n"
       "\U0001F539 What time is it? — Который час?\n"
       "\U0001F539 Today is Monday. — Сегодня понедельник.\n"
       "\U0001F539 I’ll come at 5 PM. — Я приду в 5 вечера.",
    6: "\U0001F4D8 Урок 6: Путешествие\n\n"
       "\U0001F539 Where is the hotel? — Где отель?\n"
       "\U0001F539 I need a taxi. — Мне нужно такси.\n"
       "\U0001F539 I’m lost. — Я потерялся.",
    7: "\U0001F4D8 Урок 7: Финал\n\n"
       "Ты прошёл все 7 уроков!\n"
       "Готов проверить свои знания в коротком тесте? Нажми кнопку ниже ⬇️"
}

quiz_progress = {}
user_progress = {}

quiz_questions = {
    1: {"question": "Как сказать 'Привет' на английском?", "options": ["Hello", "Bye", "Thanks"], "answer": "Hello"},
    2: {"question": "Перевод: 'How are you?'", "options": ["Где ты?", "Как дела?", "Я хорошо"], "answer": "Как дела?"},
    3: {"question": "'Меня зовут Алия' — это:", "options": ["I am Aaliya", "I name Aaliya", "My name is Aaliya"], "answer": "My name is Aaliya"},
    4: {"question": "Перевод: 'What?'", "options": ["Кто?", "Сколько?", "Что?"], "answer": "Что?"},
    5: {"question": "'Где находится отель?' — это:", "options": ["Where is the hotel?", "Who is the hotel?", "When is hotel?"], "answer": "Where is the hotel?"},
    6: {"question": "'Я потерялся' — это:", "options": ["I am lost", "I am late", "I am sad"], "answer": "I am lost"},
    7: {"question": "Перевод: 'How much is it?'", "options": ["Сколько стоит?", "Где это?", "Когда это?"], "answer": "Сколько стоит?"},
    8: {"question": "'Water, please.' — это:", "options": ["Воды, пожалуйста.", "Туалет, пожалуйста.", "Молоко, пожалуйста."], "answer": "Воды, пожалуйста."},
    9: {"question": "'Я голоден' — это:", "options": ["I’m hungry", "I’m happy", "I’m tired"], "answer": "I’m hungry"},
    10: {"question": "'Today is Monday' — это:", "options": ["Завтра понедельник", "Сегодня понедельник", "Сегодня вторник"], "answer": "Сегодня понедельник"},
    11: {"question": "'Do you have this in black?' — это:", "options": ["У вас есть это в чёрном?", "Вы это купите?", "Это моё?"], "answer": "У вас есть это в чёрном?"},
    12: {"question": "'Nice to meet you' — это:", "options": ["Приятно познакомиться", "До свидания", "Спасибо"], "answer": "Приятно познакомиться"},
    13: {"question": "'I like coffee' — это:", "options": ["Я люблю кофе", "Я пью кофе", "Я не люблю кофе"], "answer": "Я люблю кофе"},
    14: {"question": "Перевод: 'Who?'", "options": ["Почему?", "Кто?", "Когда?"], "answer": "Кто?"},
    15: {"question": "'Taxi' — это:", "options": ["Такси", "Поезд", "Машина"], "answer": "Такси"}
}

def main_keyboard():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="📖 Начать обучение")]], resize_keyboard=True)

def lesson_keyboard():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="➡ Следующий урок")]], resize_keyboard=True)

async def start_handler(message: Message):
    user_progress[message.from_user.id] = 1
    await message.answer("👋 Привет! Это бесплатный бот для изучения английского.\nТы получишь 7 коротких уроков + тест.", reply_markup=main_keyboard())

async def first_lesson_handler(message: Message):
    user_progress[message.from_user.id] = 1
    await message.answer(lessons[1], reply_markup=lesson_keyboard())

async def next_lesson_handler(message: Message):
    user_id = message.from_user.id
    day = user_progress.get(user_id, 1) + 1

    if day <= 7:
        user_progress[user_id] = day
        await message.answer(lessons[day], reply_markup=lesson_keyboard())

        if day == 7:
            await message.answer("🎉 Ты прошёл все 7 уроков!\nХочешь пройти тест? Нажми ниже ⬇️",
                                 reply_markup=ReplyKeyboardMarkup(
                                     keyboard=[[KeyboardButton(text="📊 Пройти тест")]], resize_keyboard=True))
    else:
        await message.answer("Ты уже прошёл все уроки. Хочешь пройти тест? Нажми ниже ⬇️",
                             reply_markup=ReplyKeyboardMarkup(
                                 keyboard=[[KeyboardButton(text="📊 Пройти тест")]], resize_keyboard=True))

async def start_quiz(message: Message):
    user_id = message.from_user.id
    quiz_progress[user_id] = {"q": 1, "score": 0}
    await send_quiz_question(message)

async def send_quiz_question(message: Message):
    user_id = message.from_user.id
    q_num = quiz_progress[user_id]["q"]
    data = quiz_questions[q_num]

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                   keyboard=[[KeyboardButton(text=opt)] for opt in data["options"]])
    await message.answer(f"❓ Вопрос {q_num}/15:\n{data['question']}", reply_markup=keyboard)

async def handle_quiz_answer(message: Message):
    user_id = message.from_user.id

    if user_id not in quiz_progress:
        return

    q_num = quiz_progress[user_id]["q"]
    correct = quiz_questions[q_num]["answer"]
    answer = message.text

    if answer == correct:
        quiz_progress[user_id]["score"] += 1
        await message.answer("✅ Правильно!")
    else:
        await message.answer(f"❌ Неправильно.\nПравильный ответ: {correct}")

    if q_num < 15:
        quiz_progress[user_id]["q"] += 1
        await send_quiz_question(message)
    else:
        score = quiz_progress[user_id]["score"]
        await message.answer(f"📊 Тест завершён!\nТы ответил правильно на {score} из 15 вопросов.",
                             reply_markup=ReplyKeyboardRemove())
        del quiz_progress[user_id]

async def main():
    bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.message.register(start_handler, CommandStart())
    dp.message.register(first_lesson_handler, F.text == "📖 Начать обучение")
    dp.message.register(next_lesson_handler, F.text == "➡ Следующий урок")
    dp.message.register(start_quiz, F.text == "📊 Пройти тест")
    dp.message.register(handle_quiz_answer)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
