import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, BotCommand
from deep_translator import GoogleTranslator

API_TOKEN = "7710002190:AAFkqfdSMsEYFBCUEd_kruCMQYTvm_7_bzU"  # Замените на ваш токен

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
translator = GoogleTranslator()
user_directions = {}

# Клавиатура с кнопками
language_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Русский → Турецкий")],
        [KeyboardButton(text="Турецкий → Русский")],
        [KeyboardButton(text="Помощь"), KeyboardButton(text="О проекте")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие"
)

# /start
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привет! Я русско-турецкий переводчик.\n\n"
        "Выберите направление перевода:",
        reply_markup=language_keyboard
    )

# /help и кнопка "Помощь"
@dp.message(Command("help"))
@dp.message(lambda msg: msg.text.lower() == "помощь")
async def help_command(message: types.Message):
    await message.answer(
        "📌 *Как пользоваться ботом:*\n"
        "1. Выберите направление перевода кнопкой.\n"
        "2. Отправьте текст, и я переведу его.\n\n"
        "🛠 Команды:\n"
        "/start — перезапуск\n"
        "/help — помощь\n"
        "/about — о проекте",
        parse_mode="Markdown"
    )

# /about и кнопка "О проекте"
@dp.message(Command("about"))
@dp.message(lambda msg: msg.text.lower() == "о проекте")
async def about_command(message: types.Message):
    await message.answer(
        "ℹ️ *О проекте:*\n"
        "Этот бот переводит текст между русским и турецким языками.\n"
        "Разработан с использованием Python, aiogram и Google Translate.\n"
        "Бот не хранит данные и работает мгновенно.",
        parse_mode="Markdown"
    )

# Обработка выбора направления
@dp.message(lambda msg: msg.text in ["Русский → Турецкий", "Турецкий → Русский"])
async def choose_direction(message: types.Message):
    user_directions[message.from_user.id] = message.text
    await message.answer(f"Вы выбрали: {message.text}. Теперь отправьте текст для перевода.")

# Перевод текста
@dp.message()
async def translate_text(message: types.Message):
    direction = user_directions.get(message.from_user.id)
    if not direction:
        await message.answer("Сначала выберите направление перевода:", reply_markup=language_keyboard)
        return

    src, dest = ("ru", "tr") if direction == "Русский → Турецкий" else ("tr", "ru")

    try:
        translated_text = GoogleTranslator(source=src, target=dest).translate(message.text)
        await message.answer(f"📍 Перевод:\n{translated_text}")
    except Exception as e:
        await message.answer(f"❌ Ошибка при переводе: {e}")

# Установка команд в Telegram меню
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Начать заново"),
        BotCommand(command="help", description="Инструкция по использованию"),
        BotCommand(command="about", description="О проекте"),
    ]
    await bot.set_my_commands(commands)

# Основной запуск
async def main():
    print("Настройка команд бота...")
    await set_commands(bot)
    print("Начало опроса...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()  # Закрытие сессии aiohttp
        print("Сессия бота закрыта.")


if __name__ == "__main__":
    asyncio.run(main())