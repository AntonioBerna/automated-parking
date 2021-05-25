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
reservation_button = types.KeyboardButton(db["name_reservation_button"])
markup.row(state_button, reservation_button)
markup.row(help_button)

@bot.message_handler(commands=["start"])
def send_start(message):
    bot.send_message(message.chat.id, text=db["start_text"], reply_markup=markup)

# message.text[1:len(message.text)-1] if I decide to use emoji
@bot.message_handler(commands=["state"])
@bot.message_handler(func=lambda message: message.text == db["name_state_button"])
def send_state(message):
    bot.send_message(message.chat.id, text=f"Informazioni Parcheggio\n\n{parking.getMessage()}")
    parking.giveSeats(4)

@bot.message_handler(commands=["reservation"])
@bot.message_handler(func=lambda message: message.text == db["name_reservation_button"])
def send_reservation(message):
    bot.send_message(message.chat.id, text="Inserisci il tuo nome:")
    bot.send_message(message.chat.id, text="Inserisci la data di prenotazione:")
    bot.send_message(message.chat.id, text="Inserisci l'orario:")

@bot.message_handler(commands=["help"])
@bot.message_handler(func=lambda message: message.text == db["name_help_button"])
def send_help(message):
    bot.send_message(message.chat.id, text=db["help_text"])

bot.polling()