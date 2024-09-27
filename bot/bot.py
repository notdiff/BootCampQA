import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
from transformers import pipeline
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Установите токен вашего бота
API_TOKEN = '7542935859:AAG8hoGhv9Aeei066Psv5e81ejytm9OLjs4'

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Загрузка предобученной модели QA из библиотеки transformers
qa_pipeline = pipeline("question-answering", model="check_distillBertQA_5")

# Храним состояние контекста для каждого пользователя
user_context = {}
awaiting_context = {}
print('Bot start')


# Кнопка для обновления контекста
def get_keyboard():
    keyboard = [
        [KeyboardButton(text="Новый контекст")]  # Кнопка должна быть внутри списка
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


# Обработчик команды /start
@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.answer(
        "Привет! Нажми на кнопку 'Новый контекст', чтобы отправить контекст.",
        reply_markup=get_keyboard()
    )


# Обработчик нажатия на кнопку "Новый контекст"
@dp.message(F.text == "Новый контекст")
async def ask_for_context(message: types.Message):
    user_id = message.from_user.id

    # Устанавливаем флаг, что бот ожидает новый контекст
    awaiting_context[user_id] = True
    await message.answer("Пожалуйста, отправь новый контекст.")


# Обработчик получения нового контекста
@dp.message(lambda message: message.from_user.id in awaiting_context and awaiting_context[message.from_user.id])
async def handle_new_context(message: types.Message):
    user_id = message.from_user.id
    context = message.text.strip()

    # Сохраняем новый контекст для пользователя и убираем флаг ожидания контекста
    user_context[user_id] = context
    awaiting_context[user_id] = False

    await message.answer("Контекст сохранен! Теперь можешь задать вопрос.", reply_markup=get_keyboard())


# Обработчик вопросов после получения контекста
@dp.message(
    lambda message: message.from_user.id in user_context and not awaiting_context.get(message.from_user.id, False))
async def handle_question(message: types.Message):
    user_id = message.from_user.id
    question = message.text.strip()

    # Получаем сохраненный контекст
    context = user_context.get(user_id)

    if context:
        # Используем модель для ответа на вопрос
        result = qa_pipeline({
            'question': question,
            'context': context
        })

        # Формируем ответ и отправляем его пользователю
        answer = result['answer']
        await message.answer(f"Ответ: {answer}", reply_markup=get_keyboard())
    else:
        await message.answer("Сначала отправь мне контекст.", reply_markup=get_keyboard())


# Основная функция для запуска бота
async def main():
    # Запуск бота
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


# Запуск основного цикла программы
if __name__ == '__main__':
    asyncio.run(main())