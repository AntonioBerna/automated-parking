import telebot
import serial
import time
import json

class Parking:
    def __init__(self):
        self.arduino = serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=0)
        self.delay = 2
    
    def getSeats(self):
        time.sleep(self.delay)
        seats = self.arduino.readline().decode("utf-8").strip()
        if len(seats) == 1:
            # print(f"Posti Liberi: {seats}\nlen: {len(seats)}") 
            return f"Posti Liberi: {seats}"
        else:
            return "Si è verificato un errore...Riprova!"

parking = Parking()
db = json.load(open("db.json"))
bot = telebot.TeleBot(db["token"])
print("Bot in esecuzione.")

@bot.message_handler(commands=["start"])
def send_start(message):
    bot.send_message(message.chat.id, text="Benvenuto nel Progetto di Maturità 2020/2021 di Antonio Bernardini!")

@bot.message_handler(commands=["state"])
def send_start(message):
    bot.send_message(message.chat.id, text=f"{parking.getSeats()}")

bot.polling()