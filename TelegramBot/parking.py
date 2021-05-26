import serial
import time


class Parking:
    def __init__(self):
        try:
            self.arduino = serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=0)
        except serial.serialutil.SerialException:
            print("Non è stata rilevata alcuna scheda Arduino... Riprova più tardi!")
            exit()
        self.digits = 1
        self.total_seats = 5
    
    # def giveSeats(self, seats):
    #     self.arduino.write(str(seats).encode("ascii"))
    
    def getSeats(self):
        try:
            return int(self.arduino.read(self.arduino.inWaiting()).decode("utf-8").split()[-1])
        except Exception as e:
            print(f"Errore 123... Riprova più tardi!\n{e}")
            return 123

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
