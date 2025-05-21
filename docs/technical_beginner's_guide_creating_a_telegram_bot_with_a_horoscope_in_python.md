# Техническое руководство для начинающих: Создание Telegram-бота с гороскопом на Python

---

## Введение

В этом руководстве мы шаг за шагом создадим Telegram-бота, который будет запрашивать знак зодиака и дату у пользователя и отправлять персональный гороскоп, используя публичное API.

---

## Содержание

1. [Создание Telegram-бота и получение токена](#шаг-1-создание-telegram-бота-и-получение-токена)
2. [Настройка рабочего окружения](#шаг-2-настройка-рабочего-окружения)
3. [Написание кода бота](#шаг-3-написание-кода-бота)
4. [Запуск и тестирование бота](#шаг-4-запуск-и-тестирование-бота)
5. [Архитектура и визуализация](#архитектура-и-визуализация)

---

## Шаг 1. Создание Telegram-бота и получение токена

1. В Telegram найдите бота [BotFather](https://core.telegram.org/file/811140253/1/tVdi9Kvdrp0.52332/original).
2. Отправьте команду /newbot.
3. Задайте имя и username (должен заканчиваться на bot, например myhorobot).
4. Скопируйте сгенерированный токен.


---

## Шаг 2. Настройка рабочего окружения

### 2.1 Проверка или установка Python

Проверьте, установлен ли Python:

python --version

Если нет — скачайте с [официального сайта](https://python.org).

---

### 2.2 Создание виртуального окружения

python -m venv venv

Активация:

- Windows:

    venv\Scripts\activate
  

- Linux/macOS:

    source venv/bin/activate
  

---

### 2.3 Установка библиотек

pip install pyTelegramBotAPI python-dotenv requests

---

### 2.4 Создание файла .env

BOT_TOKEN=ваш_токен_из_BotFather

---

## Шаг 3. Написание кода бота

Создайте файл main.py

```python
from dotenv import load_dotenv
from pathlib import Path
from telebot import TeleBot, types
import os
import requests
```
### Загрузка токена из .env
```python
dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=dotenv_path)
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set. Check your .env file.")

bot = TeleBot(BOT_TOKEN)
```
### Команды бота
```python
bot.set_my_commands([
    types.BotCommand("start", "Начать работу с ботом"),
    types.BotCommand("hello", "Поздороваться с ботом"),
    types.BotCommand("horoscope", "Получить гороскоп"),
])
```
### Список допустимых знаков
```python
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
```
### Команда /start и /hello
```python
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я бот-гороскоп ✨\nНапиши /horoscope чтобы получить прогноз.")
```
### Команда /horoscope
```python
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
```
### Получение данных из API
```python
def get_daily_horoscope(sign: str, day: str) -> dict:
    url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
    params = {"sign": sign, "day": day}
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
```
### Обработчик по умолчанию
```python
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, "Неизвестная команда. Напишите /horoscope для гороскопа.")
```
### Запуск
```python
bot.infinity_polling()
```
---

## Шаг 4. Запуск и тестирование бота

python main.py

Откройте Telegram, найдите вашего бота, напишите /start и следуйте подсказкам.

---

## Архитектура и визуализация

### Структура проекта

src/
├── main.py
├── .env


---

### Диаграмма последовательности

sequenceDiagram
    participant User
    participant Bot
    participant API

    User->>Bot: /horoscope
    Bot->>User: Ввод знака
    User->>Bot: Aries
    Bot->>User: Ввод дня
    User->>Bot: Today
    Bot->>API: Запрос гороскопа
    API-->>Bot: Гороскоп
    Bot->>User: Ответ с гороскопом

---

### Потоковая диаграмма

flowchart TD
    A[Пользователь вводит /horoscope] --> B[Бот спрашивает знак]
    B --> C[Пользователь вводит знак]
    C --> D[Бот спрашивает дату]
    D --> E[Пользователь вводит дату]
    E --> F[Бот делает запрос к API]
    F --> G[Получает и выводит гороскоп]

---

