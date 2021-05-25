from random import *
import datetime
import string
import serial
import qrcode
import time
import json


class Parking:
    def __init__(self):
        try:
            self.arduino = serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=0)
        except serial.serialutil.SerialException:
            print("Non è stata rilevata alcuna scheda Arduino... Riprova più tardi!")
            exit()
        self.delay = 2
        self.digits = 1 # 2 ?!
        self.total_seats = 5
    
    def giveSeats(self, seats):
        self.arduino.write(str(seats).encode("ascii"))
    
    def getSeats(self):
        try:
            time.sleep(self.delay)
            self.seats = int(self.arduino.readline().decode("utf-8").strip())
            return self.seats
        except Exception as e:
            print(f"Errore 123... Riprova più tardi!\n{e}")
            return 123
            exit()

    def getMessage(self):
        current_seats = self.getSeats()
        hour = time.strftime("%H:%M:%S")
        date = time.strftime("%d/%m/%Y")
        if len(str(current_seats)) == self.digits:
            if current_seats > 0:
                return f"Posti Disponibili: {current_seats}\nPosti Totali: {self.total_seats}\n\nUltimo Aggiornamento:\n{date} {hour}"
            else:
                return f"Il parcheggio è pieno!\nRiprova più tardi...\n\nUltimo Aggiornamento:\n{date} {hour}"
        else:
            return "Si è verificato un errore... Riprova più tardi!"


class Reservation:
    def __init__(self, data_user):
        self.name = None
        self.date = None
        self.hour = None
        self.current_date = time.strftime("%d/%m/%Y")

        self.reservation = json.load(open("reservation.json"))
        self.matrix = []
    
    def addReservation(self, chat_id, data_user):
        self.matrix.append(data_user)
        print(self.matrix)
        self.reservation[chat_id] = self.matrix
        with open("reservation.json", "w") as json_file:
            json.dump(self.reservation, json_file, indent=2)
    
    def checkDate(self, date, date_format):
        if datetime.datetime.strptime(date, date_format):
            day, month, year = tuple(date.split("/"))
            current_day, current_month, current_year = tuple(self.current_date.split("/"))
            if (year == current_year and month == current_month  and day == current_day) or \
            (year == current_year and month == current_month  and day > current_day) or \
            (year == current_year and month > current_month) or \
            (year > current_year):
                return 1
        else:
            return 0
        
    def randomCode(self):
        return "".join(choice(string.digits) for x in range(8))


class QRCodeMaker:
    def __init__(self, text):
        self.text = " ".join(text)
    
    def make(self):
        return qrcode.make(self.text).get_image()