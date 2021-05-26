from random import *
import datetime
import string
import json
import time


class Reservation:
    def __init__(self, data_user):
        self.name = None
        self.date = None
        self.hour = None
        self.current_date = time.strftime("%d/%m/%Y")
    
    def addReservation(self, chat_id, data_user):
        reservation = json.load(open("reservation.json"))
        
        if chat_id not in reservation.keys():
            reservation[chat_id] = []
        reservation[chat_id].append(date_user)

        with open("reservation.json", "w") as file:
            json.dump(self.reservation, file, indent=2)
    
    def checkDate(self, date):
        try:
            datetime.datetime.strptime(date, "%d/%m/%Y"):
            day, month, year = tuple(date.split("/"))
            current_day, current_month, current_year = tuple(self.current_date.split("/"))

            if (year == current_year and month == current_month  and day == current_day) or \
            (year == current_year and month == current_month  and day > current_day) or \
            (year == current_year and month > current_month) or \
            (year > current_year):
                return 1
            else:
                return 0
        except ValueError:
            return 0
        
    def randomIdentifier(self):
        return "".join(choice(string.digits) for x in range(8))