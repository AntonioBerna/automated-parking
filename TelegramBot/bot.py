from parking import Parking
from telebot import types
import telebot
import json


parking = Parking()
db = json.load(open("db.json"))
bot = telebot.TeleBot(db["token"])
print("Bot in esecuzione.")

markup = types.ReplyKeyboardMarkup()
state_button = types.KeyboardButton(db["name_state_button"])
markup.row(state_button)

@bot.message_handler(commands=["start"])
def send_start(message):
    bot.send_message(message.chat.id, text=db["start_text"], reply_markup=markup)

@bot.message_handler(commands=["state"])
# message.text[1:len(message.text)-1]
@bot.message_handler(func=lambda message: message.text == db["name_state_button"])
def send_state(message):
    seats = parking.getSeats()
    if len(str(seats)) == 1:
        if seats > 0:
            bot.send_message(message.chat.id, text=f"Posti Liberi: {seats}")
        else:
            bot.send_message(message.chat.id, text="Il Parcheggio è pieno!")
    else:
        bot.send_message(message.chat.id, text="Si è verificato un errore...Riprova!")

bot.polling()