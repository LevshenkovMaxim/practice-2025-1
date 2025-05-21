from dotenv import load_dotenv
from pathlib import Path
from telebot import TeleBot, types
import os
import requests

# Загрузка токена из .env
dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=dotenv_path)
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set. Check your .env file.")

bot = TeleBot(BOT_TOKEN)

# Команды бота
bot.set_my_commands([
    types.BotCommand("start", "Начать работу с ботом"),
    types.BotCommand("hello", "Поздороваться с ботом"),
    types.BotCommand("horoscope", "Получить гороскоп"),
])

# Список допустимых знаков
ZODIAC_SIGNS = {
    "Овен": "Aries",
    "Телец": "Taurus",
    "Близнецы": "Gemini",
    "Рак": "Cancer",
    "Лев": "Leo",
    "Дева": "Virgo",
    "Весы": "Libra",
    "Скорпион": "Scorpio",
    "Стрелец": "Sagittarius",
    "Козерог": "Capricorn",
    "Водолей": "Aquarius",
    "Рыбы": "Pisces",
}

DAYS = ["TODAY", "TOMORROW", "YESTERDAY"]

# Команда /start и /hello
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я бот-гороскоп ✨\nНапиши /horoscope чтобы получить прогноз.")

# Команда /horoscope
@bot.message_handler(commands=['horoscope'])
def horoscope_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for sign in ZODIAC_SIGNS.keys():
        markup.add(sign)
    bot.send_message(message.chat.id, "Выберите ваш знак зодиака:", reply_markup=markup)
    bot.register_next_step_handler(message, ask_day)

def ask_day(message):
    user_sign = message.text
    if user_sign not in ZODIAC_SIGNS:
        bot.send_message(message.chat.id, "❗️ Неверный знак. Попробуйте снова с /horoscope")
        return
    sign_en = ZODIAC_SIGNS[user_sign]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row("TODAY", "TOMORROW", "YESTERDAY")
    bot.send_message(message.chat.id, "Выберите день:", reply_markup=markup)
    bot.register_next_step_handler(message, fetch_horoscope, sign_en)

def fetch_horoscope(message, sign_en):
    day = message.text.upper()
    if day not in DAYS:
        bot.send_message(message.chat.id, "❗️ Неверный день. Попробуйте снова с /horoscope")
        return

    horoscope = get_daily_horoscope(sign_en, day)

    if "error" in horoscope:
        bot.send_message(message.chat.id, "🚫 Ошибка при получении гороскопа. Попробуйте позже.")
        return

    data = horoscope["data"]
    text = f"🔮 *Гороскоп для {sign_en}*\n📅 *{data['date']}*\n\n_{data['horoscope_data']}_"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

# Получение данных из API
def get_daily_horoscope(sign: str, day: str) -> dict:
    url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
    params = {"sign": sign, "day": day}
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Обработчик по умолчанию
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, "Неизвестная команда. Напишите /horoscope для гороскопа.")

# Запуск
bot.infinity_polling()