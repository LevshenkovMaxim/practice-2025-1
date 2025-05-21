# Модификация и развитие проекта Telegram-бота с гороскопом на Python

---

## 1. Настройка команд Telegram-бота

Цель: Сделать список команд более информативным и удобным для пользователя.

Что нужно сделать:

- Обновлять команды бота через метод set_my_commands.
- Добавить команды для помощи, настроек и справки.


```python
from telebot import types

commands = [
    types.BotCommand("start", "Начать работу с ботом"),
    types.BotCommand("hello", "Поздороваться с ботом"),
    types.BotCommand("horoscope", "Получить гороскоп"),
]

bot.set_my_commands(commands)
```

## 2. Обработчик сообщений по умолчанию
Цель: Обрабатывать непонятные сообщения и помогать пользователю.

Что нужно сделать:

Добавить ответ по умолчанию, который подсказывает доступные команды.

```python
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, "Неизвестная команда. Напишите /horoscope для гороскопа.")
```
