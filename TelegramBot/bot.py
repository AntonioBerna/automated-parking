from parking import Parking
from telebot import types
import telebot
import json

parking = Parking()
db = json.load(open("db.json"))
bot = telebot.TeleBot(db["token"])
print("Bot in esecuzione.")

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
state_button = types.KeyboardButton(db["name_state_button"])
help_button = types.KeyboardButton(db["name_help_button"])
markup.row(state_button, help_button)

@bot.message_handler(commands=["start"])
def send_start(message):
    bot.send_message(message.chat.id, text=db["start_text"], reply_markup=markup)

@bot.message_handler(commands=["state"])
@bot.message_handler(func=lambda message: message.text == db["name_state_button"]) # message.text[1:len(message.text)-1]
def send_state(message):
    seats = parking.getSeats()
    total_seats = parking.getTotalSeats()

    if len(str(seats)) == 1 and seats > 0:
        bot.send_message(message.chat.id, text=f"Informazioni Parcheggio\n\n{parking.getMessage()}")
    else:
        bot.send_message(message.chat.id, text=f"Informazioni Parcheggio\n\n{parking.getMessage()}")

@bot.message_handler(commands=["help"])
@bot.message_handler(func=lambda message: message.text == db["name_help_button"])
def send_help(message):
    bot.send_message(message.chat.id, text=db["help_text"])

bot.polling()