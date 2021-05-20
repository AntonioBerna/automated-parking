import serial
import time

class Parking:
    def __init__(self):
        self.arduino = serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=0)
        self.delay = 2
    
    def getSeats(self):
        time.sleep(self.delay)
        return int(self.arduino.readline().decode("utf-8").strip())