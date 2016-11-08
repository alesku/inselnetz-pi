#!/usr/bin/python
# -*- coding: utf-8 -*-

# Das Programm stellt eine Verbindung mit dem OutBack MATE her.
# Danach liest sie eine Zeile Daten vom dem MATE und gleichzeitig
# schreibt die unveränderte Zeile in die .csv Datei.
# Lese/Schreibvorgang geschieht jede Sekunde.

import serial

MATE = serial.Serial(
    port = '/dev/ttyUSB2',
    baudrate = 19200,
    bytesize = serial.EIGHTBITS,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    timeout = 1
    )

# Man muss das implizit setzen, sonst werden keine Daten geliefert.
MATE.setRTS(False)


#print ("Connected to: " + mate.portstr)

while True:
	try:
		zeile = MATE.readline()
		aktualdaten = open("/home/pi/Inselnetz/FLEXmax60/Daten/Aktual_MATE.csv", "w")
		aktualdaten.write(zeile)
		aktualdaten.close()

	except:
		print
