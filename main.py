import telebot
import time
import os

TOKEN = "8358189287:AAEgpx2S0d6ub8oc_dCT5YJp-wVbfY3ZjH0"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "🤖 مرحبا!\nالبوت راهو خدام بنجاح ✅"
    )

print("Bot is running...")

while True:
    try:
        bot.polling(non_stop=True)
    except Exception as e:
        print("Error:", e)
        time.sleep(5)
