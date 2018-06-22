import sys
import webbrowser
import serial

device = sys.argv[1]
ser = serial.Serial(device)

while True:
    url = ser.readline()
    webbrowser.open(url)
