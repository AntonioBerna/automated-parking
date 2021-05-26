from parking import Parking
from qrcodemaker import QRCodeMaker
from reservation import Reservation
from telebot import types
import telebot
import json


data_user = {}
parking = Parking()
user = Reservation()
db = json.load(open("db.json"))
bot = telebot.TeleBot(db["token"], parse_mode="HTML")
print("Bot in esecuzione.")


@bot.message_handler(commands=["start"])
def send_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    state_button = types.KeyboardButton(db["name_state_button"])
    help_button = types.KeyboardButton(db["name_help_button"])
    reservation_button = types.KeyboardButton(db["name_reservation_button"])
    markup.row(state_button, reservation_button)
    markup.row(help_button)
    bot.send_message(message.chat.id, text=db["start_text"], reply_markup=markup)

# message.text[1:len(message.text)-1] if I decide to use emoji
@bot.message_handler(commands=["state"])
@bot.message_handler(func=lambda message: message.text == db["name_state_button"])
def send_state(message):
    bot.send_message(message.chat.id, text=f"Informazioni Parcheggio\n\n{parking.getMessage()}")

@bot.message_handler(commands=["reservation"])
@bot.message_handler(func=lambda message: message.text == db["name_reservation_button"])
def send_reservation(message):
    msg = bot.send_message(message.chat.id, text="Inserisci il tuo nome:")
    bot.register_next_step_handler(msg, process_name_step)

def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user.name = name
        data_user["name"] = user.name
        msg = bot.send_message(chat_id, text="Per quando vuoi prenotare il parcheggio? (gg/mm/aaaa)")
        bot.register_next_step_handler(msg, process_date_step)
    except Exception as e:
        print("Si è verificato un errore... Riprova più tardi!")
        bot.send_message(chat_id, "Si è verificato un errore... Riprova più tardi!")

def process_date_step(message):
    try:
        chat_id = message.chat.id
        date = message.text
        if parking.getSeats() > 0:
            if user.checkDate(date):
                identifier = user.randomIdentifier()
                qr_code = QRCodeMaker(identifier)
                user.date = date
                data_user["date"] = user.date
                user.addReservation(chat_id, data_user)
                bot.send_photo(chat_id, photo=qr_code.make(), caption=f"Prenotazione effettuata!\n\nNome: {user.name}\nData prenotazione: {user.date}\nID: {identifier}")
            else:
                msg = bot.send_message(chat_id, text="Data inserita non è valida... Riprova!\n\nPer quando vuoi prenotare il parcheggio? (gg/mm/aaaa)")
                bot.register_next_step_handler(msg, process_date_step)
        else:
            bot.send_message(message.chat.id, text=f"Il parcheggio è pieno!\nRiprova più tardi...")
    except Exception as e:
        print(f"Si è verificato un errore... Riprova più tardi!\n{e}")
        bot.send_message(chat_id, "Si è verificato un errore... Riprova più tardi!")

@bot.message_handler(commands=["help"])
@bot.message_handler(func=lambda message: message.text == db["name_help_button"])
def send_help(message):
    bot.send_message(message.chat.id, text=db["help_text"])

bot.polling()