from parking import Parking
from telebot import types
import telebot
import json


parking = Parking()
db = json.load(open("db.json"))
bot = telebot.TeleBot(db["token"], parse_mode="HTML")
print("Bot in esecuzione.")

@bot.message_handler(commands=["start"])
def send_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    state_button = types.KeyboardButton(db["name_state_button"])
    help_button = types.KeyboardButton(db["name_help_button"])
    markup.row(state_button)
    markup.row(help_button)
    bot.send_message(message.chat.id, text=db["start_text"], reply_markup=markup)

@bot.message_handler(commands=["state"])
@bot.message_handler(func=lambda message: message.text == db["name_state_button"])
def send_state(message):
    current_seats = parking.getSeats()
    bot.send_message(message.chat.id, text=f"Informazioni Parcheggio\n\n{parking.getMessage(current_seats)}")

@bot.message_handler(commands=["help"])
@bot.message_handler(func=lambda message: message.text == db["name_help_button"])
def send_help(message):
    bot.send_message(message.chat.id, text=db["help_text"])

bot.polling()