import serial
import time

class Parking:
    def __init__(self):
        try:
            self.arduino = serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=0)
        except serial.serialutil.SerialException:
            print("Non è stata rilevata alcuna scheda Arduino... Riprova più tardi!")
            exit()
        
        self.delay = 2
        self.seats = -1
        self.digits = 1 # 2 ?!
        self.total_seats = 5
        self.hour = time.strftime("%H:%M:%S")
        self.date = time.strftime("%d/%m/%Y")
    
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
        if len(str(current_seats)) == self.digits:
            if current_seats > 0:
                return f"Posti Disponibili: {current_seats}\nPosti Totali: {self.total_seats}\n\nUltimo Aggiornamento:\n{self.date} {self.hour}"
            else:
                return f"Il parcheggio è pieno!\nRiprova più tardi...\n\nUltimo Aggiornamento:\n{self.date} {self.hour}"
        else:
            return "Si è verificato un errore... Riprova più tardi!"