import requests
import telebot
from decouple import config
from apps.tg.models import TelegramUser, update_feedback


TOKEN = config('TOKEN')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def message_send(message):
    bot.reply_to(message, "Добро пожаловать в нашу курьерскую службу доставки! 🚚💨 Ниже будет ссылка на группу,"
                          "там вы можете отслеживать свои доставки и получать важные обновления. Начнем вместе"
                          "сделаем доставку быстрой и удобной! 📦💼")


@bot.message_handler(commands=['help'])
def message_send(message):
    help_text = (
        "Это бот курьерской службы доставки. Используйте следующие команды:\n"
        "/start - Начать взаимодействие с ботом.\n"
        "/help - Получить этот текст справки.\n"
        "/orders - Просмотреть доступные заказы.\n"
        "/contact - Связаться с поддержкой или администрацией.\n"
        "/feedback - Оставить отзыв или обратную связь."
    )

    bot.reply_to(message, help_text)
@bot.message_handler(commands=['contact'])
def message_send(message):
    contact_text = (
        "Свяжитесь с нами для поддержки или вопросов:\n"
        "Телефон: +996552590770\n"
        "Telegram: @trueBella"
    )
    bot.reply_to(message, contact_text)

@bot.message_handler(commands=['feedback'])
def message_send(message):
    bot.reply_to(message, "Оставьте свой отзыв или комментарий!")


@bot.message_handler(func=lambda message: True)
def handle_feedback(message):
    user_id = int(message.from_user.id)
    user_feedback = message.text

    # Сохраняем отзыв в базе данных
    update_feedback(user_id, user_feedback)
    bot.reply_to(message, "Спасибо за ваш отзыв! Ваше мнение очень важно для нас.")











