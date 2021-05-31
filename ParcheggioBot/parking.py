import serial
import time


class Parking:
    def __init__(self):
        self.total_seats = 5
        
        try:
            self.arduino = serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=0)
        except serial.serialutil.SerialException:
            print("Non è stata rilevata alcuna scheda Arduino... Riprova più tardi!")
            exit()
    
    def getSeats(self):
        try:
            return int(self.arduino.read(self.arduino.inWaiting()).decode("utf-8").split()[-1])
        except Exception as e:
            print(f"Si è verificato un errore... Riprova più tardi!\n{e}")
            exit()

    def getMessage(self, current_seats):
        try:
            hour = time.strftime("%H:%M:%S")
            date = time.strftime("%d/%m/%Y")
            if current_seats > 0:
                return f"Posti Disponibili: {current_seats}\nPosti Totali: {self.total_seats}\n\nUltimo Aggiornamento:\n{date} {hour}"
            else:
                return f"Il parcheggio è pieno!\n\nUltimo Aggiornamento:\n{date} {hour}"
        except Exception as e:
            return f"Si è verificato un errore... Riprova più tardi!\n{e}"
