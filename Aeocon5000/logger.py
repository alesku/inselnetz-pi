#/usr/lib/python
# -*- coding: utf-8 -*-
# Laut Magic String kann man Umlaute für Kommentare verwenden.

# Datei aeocon_datalogger.py, Version 1.1 vom 18.03.2016 bei Alexey Müller
# Verwendet Python 2.7.9

import serial
import struct
import numpy as np
import time
from datetime import datetime
import traceback
import binascii
import re
import math
import csv  # Bibliothek zum erstellen von CSV-Dateien
import os, sys  # Bibliothek fuer Betriebssytemoperationen

import random
#------------------------------------------------------------------------------

#konfiguration serielle Schnitstelle
port = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=56000,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0.25
    )
#------------------------------------------------------------------------------

#Kommandoblock: Datenobjekt lesen (9 Byte)
#Erste 5 Byte (Konstant!)
kommando_read='\x00\x06\x02\x01\x0B'
#weitere 4 Bytes werden separat fuer jeden Objekt definiert
#Gelesene Objekt:
#Erste 5 Bytes (Konstant!) für kontrollzwecke
data_readed='\x00\x08\x01\x02\x8B'
#Weitere 6 Bytes enthalten: Sizecode:   0x00 für 32Bit (4 Byte)
#                                       0x08 für 16Bit (2 Byte)
#                                       0x0C für 8Bit  (1 Byte)
#                           Data_0 ... Dat_3
#                           Check
#------------------------------------------------------------------------------

#Funktion I_Netz()
#Einspeisestrom (Index=52 (0x34)) in [0.01 A]

def I_Netz() :   
    port.close()
    port.open()
  
    kommando_ges='\x00\x06\x02\x01\x0b\x34\x00\x00\xb7'
    
    port.write(kommando_ges)
    read_string=port.read(11)

    t=time.localtime()
    ti=str(t[3])+':'+str(t[4])+':'+str(t[5])+'-'+str(t[2])+'.'+str(t[1])+'.'+str(t[0])
    #Ueberpruefung korrekter laenge
    
    if len(read_string)==11:

        #Zurueckgelieferter Generatorfrequenz aus den bytes 6-9 
        var_1 = read_string[9]  
        var_2 = read_string[8]
        var_3 = read_string[7]
        var_4 = read_string[6]
        
        string=var_1+var_2+var_3+var_4
        help=struct.unpack(">i",string)
        Einspeisestrom=float(help[0]*0.01)
        
        return [round(Einspeisestrom, 2),ti]
    else:
        return ["Fehler lesen Generatorspannung",ti,read_string]
#------------------------------------------------------------------------------
    
#Funktion U_WEA()
#Generatorspannung (Index=55 (0x37)) in [0.1 V_DC]
def U_WEA() :   
    port.close()
    port.open()
  
    kommando_ges='\x00\x06\x02\x01\x0b\x37\x00\x00\xb4'
    
    port.write(kommando_ges)
    read_string=port.read(11)

    t=time.localtime()
    ti=str(t[3])+':'+str(t[4])+':'+str(t[5])+'-'+str(t[2])+'.'+str(t[1])+'.'+str(t[0])
    #Ueberpruefung korrekter laenge
    
    if len(read_string)==11:

        #Zurueckgelieferter Generatorfrequenz aus den bytes 6-9 
        var_1 = read_string[9]  
        var_2 = read_string[8]
        var_3 = read_string[7]
        var_4 = read_string[6]
        
        string=var_1+var_2+var_3+var_4
        help=struct.unpack(">i",string)
        Generatorspannung=float(help[0]*0.1)
        
        return [round(Generatorspannung, 2),ti]
    else:
        return ["Fehler lesen Generatorspannung",ti,read_string]
#------------------------------------------------------------------------------
    
#Funktion n_WEA()
#Generatorfrequenz (Index=53 (0x35)) in [0.01Hz]
def n_WEA() :   
    port.close()
    port.open()
    kommando_ges='\x00\x06\x02\x01\x0b\x35\x00\x00\xb6'
    port.write(kommando_ges)
    read_string=port.read(11)

    #Zeitstempel der Messung
    t=time.localtime()
    ti=str(t[3])+':'+str(t[4])+':'+str(t[5])+'-'+str(t[2])+'.'+str(t[1])+'.'+str(t[0])

    #Ueberpruefung korrekter laenge
    if len(read_string)==11:

        #Zurueckgelieferter Generatorfrequenz aus den bytes 6-9 
        var_1 = read_string[9]  
        var_2 = read_string[8]
        var_3 = read_string[7]
        var_4 = read_string[6]
        
        string=var_1+var_2+var_3+var_4
        help=struct.unpack(">i",string)
        Drehzahl_rotor=float(help[0]*0.01*60/8)# *0.01Hz*60min⁻1/8Polpaar
        
        return [round(Drehzahl_rotor,2),ti]
    else:
        return ["Fehler lesen Generatorfrequenz",ti,read_string]
#------------------------------------------------------------------------------

#Funktion: P_Netz()
#EINSPEISELEISTUNG (Index=49 (0x31)) in [0.1W]
#Einlesen der Einspeiseleistung
def P_Netz() :   
    port.close()
    port.open()
    kommando_ges='\x00\x06\x02\x01\x0b\x31\x00\x00\xba'
    
    port.write(kommando_ges)
    read_string=port.read(11)
    #antwrtblock enthaelt 
    #Zeitstempel der Messung
    t=time.localtime()
    ti=str(t[3])+':'+str(t[4])+':'+str(t[5])+'-'+str(t[2])+'.'+str(t[1])+'.'+str(t[0])
    #Ueberpruefung korrekter laenge
    
    if len(read_string)==11:

        #Zurueckgelieferter Einspeiseleistung aus den bytes 6-9 
        var_1 = read_string[9]  
        var_2 = read_string[8]
        var_3 = read_string[7]
        var_4 = read_string[6]
        
        string=var_1+var_2+var_3+var_4
        help=struct.unpack(">i",string)
        Einspeiseleistung=float(help[0]*0.1)
        
        return [round(Einspeiseleistung, 2),ti]
    else:
        return ["Fehler lesen Einspeiseleistung",ti, read_string]
#------------------------------------------------------------------------------

#Funktion P_Heiz()
#LEISTUNG UEBER BREMSWIDERSTAND (Index=246 (0xF6)) in [0.1W]
#Einlesen der Einspeiseleistung
def P_Heiz() :   
    port.close()
    port.open()
    #Definition der letzten 4 Byte: Index_Low, Index_High, Subindex, Check   
    Index_Low=0xf6
    Index_High=0x00
    Subindex=0x00
    Check=0xFF-(9+0x0B+Index_Low+Index_High+Subindex)+256#+256 da ein negatives Zahl kommt
    kommando_ges=kommando_read+chr(Index_Low)+chr(Index_High)+chr(Subindex)+chr(Check)

    
    port.write(kommando_ges)
    read_string=port.read(11)
    #antwrtblock enthaelt 
    #Zeitstempel der Messung
    t=time.localtime()
    ti=str(t[3])+':'+str(t[4])+':'+str(t[5])+'-'+str(t[2])+'.'+str(t[1])+'.'+str(t[0])

    #Ueberpruefung korrekter laenge
    if len(read_string)==11:

        #Zurueckgelieferter Leistung ueber Bremswiderstand aus den bytes 6-9 
        var_1 = read_string[9]  
        var_2 = read_string[8]
        var_3 = read_string[7]
        var_4 = read_string[6]
        
        string=var_1+var_2+var_3+var_4
        help=struct.unpack(">i",string)
        Heiz_Leistung=float(help[0])
        
        return [round(Heiz_Leistung, 2),ti]
    else:
        return ["Fehler lesen Leistung ueber Bremswiderstand",ti,read_string]
#------------------------------------------------------------------------------

#Globale Wariablen
sec_alt = datetime.now().second
minute_alt = datetime.now().minute
stunde_alt = datetime.now().hour

pfad="/home/pi/Inselnetz/Aeocon5000/Daten/"
file_csv= "_Aeocon_Daten.csv"
file_7d= "Letzte7Tage.csv"
file_30d="Letzte30Tage.csv"
file_1y= "_Jahr.csv"
file_log = "Log_aeocon.txt"

class aeocon:
    Einspeisestrom = []
    Einspeiseleistung = []
    Generatordrehzahl = []
    Generatorspannung = []
    Leistung_Heiz = []
    
# Alle drei Sekunden
def dreisekuendlich():
    daten = abfrage()
    aktualdaten_schreiben(daten)

# Alle zehn Minuten
def zehnminuetlich():
    daten = zehn_minuten_mittel()
    arrays_leeren()
    csv_schreiben(dateiname=pfad+datumsstring()+file_csv, daten=daten)

# Jede Stunde
def stuendlich():
    stundenmittel=letzte_x_werte_csv(anz_werte=6, dateiname=pfad+datumsstring()+file_csv)
    csv_schreiben_umlauf(dateiname=pfad+file_7d, daten=stundenmittel,
                                  max_anz_werte=168)

# Alle vier Stunden
def vierstuendlich():
    vierstundenmittel=letzte_x_werte_csv(anz_werte=4, dateiname=pfad+file_7d)
    csv_schreiben_umlauf(dateiname=pfad+file_30d, daten=vierstundenmittel,
                                  max_anz_werte=180)

# Jeden Tag
def taeglich():
    vierstundenmittel=letzte_x_werte_csv(anz_werte=6, dateiname=pfad+file_30d)
    datum = datetime.now().date()
    jahr = datum.strftime('%Y')
    csv_schreiben_umlauf(dateiname=pfad+jahr+file_1y, daten=vierstundenmittel,
                              max_anz_werte=365)
#------------------------------------------------------------------------------   
# Liefert Datumstring zurueck
def datumsstring():
    datum = datetime.now().date()
    datum_str = datum.strftime('%Y-%m-%d')
    return datum_str

# Pruefen ob alle Daten in Liste vollstaendig
def listencheck(liste):
    anzahl_elemente = len(liste)
    gueltig = 1
    for a in range(anzahl_elemente):
        if math.isnan(liste[a]):
            gueltig = 0
    liste.insert(0, gueltig)
    return liste

# Schreiben der eben ausgelesenen Daten in die CSV-Datei, zur Anzeige der Gauges
def aktualdaten_schreiben(daten):
    try:
        writer = csv.writer(open("/home/pi/Inselnetz/Aeocon5000/Daten/Aktualdaten.csv", "wb"), delimiter=";")
        writer.writerow(daten)
    except:
        logeintrag("Aktualdaten schreiben Fehler: " + traceback.format_exc())

# Erstellt neue CSV Datei
def csv_erstellen(dateiname):
    """
    Erstellt eine neue CSV Datei mit Bezeichnungen in der Kopfzeile
    """
    try:
        writer = csv.writer(open(dateiname, "wb"), delimiter=";")
        writer.writerow(["Datum Uhrzeit", "Epochenzeit", "1 = Daten vollstaendig", "I_Netz", "I_Netz min",
                         "I_Netz max", "P_Netz", "P_Netz min", "P_Netz max", "n_WEA", "n_WEA min",
                         "n_WEA max", "U_WEA", "U_WEA min", "U_WEA max", "P_Heiz", "P_Heiz min", "P_Heiz max"])
    except:
        logeintrag("CSV erstellen Fehler: " + traceback.format_exc())


# Schreibt in neue Zeile einer CSV-Datei
def csv_schreiben(dateiname, daten):
    """
    Zuerst wird geprueft ob die Datei schon verhanden ist.
    Falls nicht wird sie neu erstellt mit den Bezeichnungen in der Kopfzeile
    Vor den Daten wird ein Zeitstempel und die Epochenzeit (Zeit in ms seit 1970) eingefuegt
    """
    try:
        if os.path.exists(dateiname) == 0:
            print ("Neue Datei wird erstellt: " + dateiname)
            csv_erstellen(dateiname)
        writer = csv.writer(open(dateiname, "a"), delimiter=";")
        epochtime = time.time()
        daten.insert(0, epochtime)
        dt = datetime.now()
        daten.insert(0, dt.strftime('%Y-%m-%d %H:%M:%S'))
        writer.writerow(daten)
    except:
        logeintrag("CSV schreiben Fehler: " + traceback.format_exc())

# Schreibt in neue Zeile einer CSV-Datei mit max Anzahl an Werten
def csv_schreiben_umlauf(dateiname, daten, max_anz_werte):
    """
    Zuerst wird geprueft ob die Datei schon verhanden ist.
    Falls nicht wird sie neu erstellt mit den Bezeichnungen in der Kopfzeile
    Wird die max Anzahl an Werte ueberschritten wird die erste Zeile mit Daten geloescht
    Vor den Daten wird ein Zeitstempel und die Epochenzeit (Zeit in ms seit 1970) eingefuegt
    """
    try:
        if os.path.exists(dateiname) == 0:
            print ("Neue Datei wird erstellt")
            csv_erstellen(dateiname)
        csvreader = csv.reader(open(dateiname, 'rb'), delimiter=";")
        zeilenanzahl = 0
        gelesene_daten = []
        for zeile in csvreader:
            gelesene_daten.append(zeile)
            zeilenanzahl += 1
        while zeilenanzahl-1 > max_anz_werte:
            del gelesene_daten[1]
            zeilenanzahl -= 1
        writer = csv.writer(open(dateiname, "wb"), delimiter=";")
        writer = csv.writer(open(dateiname, "a"), delimiter=";")
        for zeile in range(zeilenanzahl):
            writer.writerow(gelesene_daten[zeile])
        epochtime = time.time()
        daten.insert(0, epochtime)
        dt = datetime.now()
        daten.insert(0, dt.strftime('%Y-%m-%d %H:%M:%S'))
        writer.writerow(daten)
    except:
        logeintrag("CSV schreiben Umlauf Fehler: " + traceback.format_exc())


# Liest die letzen x Werte aus einer CSV Datei und mittelt diese
def letzte_x_werte_csv(anz_werte, dateiname):
    """
    Oeffnet die Datei und versucht die letzten X Werte aus der Datei zu lesen
    Wird keine Datei mit dem Namen gefunden wird float('nan') zurueckgegeben und die Funktion beendet
    Nach erfolgreichen Oeffnen werden die Werte zugeordnet gemittelt und zuruekgegeben
    """
    try:
        csvreader = csv.reader(open(dateiname, 'rb'), delimiter=";")
    except:
        logeintrag("Letze x Werte Fehler: " + traceback.format_exc())
        return [float('nan')]
    gelesene_daten = []
    zeilenanzahl = 0
    for row in csvreader:
        gelesene_daten.append(row)
        zeilenanzahl += 1
    letztexwerte = []
    if zeilenanzahl - 1 < anz_werte:
        logeintrag("Letze x Werte Fehler: Zu wenig Eintraege vorhanden")
        for x in range(1, zeilenanzahl):
            letztexwerte.append(gelesene_daten[x])
    else:
        for x in range(zeilenanzahl - anz_werte, zeilenanzahl):
            letztexwerte.append(gelesene_daten[x])
    gelesene_daten[:] = []  # Daten leoschen um Speicher freizugeben
    zeilen = len(letztexwerte)
    spalten = len(letztexwerte[0])
    if spalten < 18:
        logeintrag("Letze x Werte Fehler: Zu wenig Spalten vorhanden")
        return [float('nan')]
    lok_Einspeisestrom_mittel = []
    lok_Einspeisestrom_min = []
    lok_Einspeisestrom_max = []
    lok_Einspeiseleistung_mittel = []
    lok_Einspeiseleistung_min = []
    lok_Einspeiseleistung_max = []
    lok_Generatordrehzahl_mittel = []
    lok_Generatordrehzahl_min = []
    lok_Generatordrehzahl_max = []
    lok_Generatorspannung_mittel = []
    lok_Generatorspannung_min = []
    lok_Generatorspannung_max = []
    lok_Leistung_Heiz_mittel = []
    lok_Leistung_Heiz_min = []
    lok_Leistung_Heiz_max = []
    for zeile in range(zeilen):  # Werte in jeweils ein Array packen
        lok_Einspeisestrom_mittel.append(float(letztexwerte[zeile][3]))
        lok_Einspeisestrom_min.append(float(letztexwerte[zeile][4]))
        lok_Einspeisestrom_max.append(float(letztexwerte[zeile][5]))
        lok_Einspeiseleistung_mittel.append(float(letztexwerte[zeile][6]))
        lok_Einspeiseleistung_min.append(float(letztexwerte[zeile][7]))
        lok_Einspeiseleistung_max.append(float(letztexwerte[zeile][8]))
        lok_Generatordrehzahl_mittel.append(float(letztexwerte[zeile][9]))
        lok_Generatordrehzahl_min.append(float(letztexwerte[zeile][10]))
        lok_Generatordrehzahl_max.append(float(letztexwerte[zeile][11]))
        lok_Generatorspannung_mittel.append(float(letztexwerte[zeile][12]))
        lok_Generatorspannung_min.append(float(letztexwerte[zeile][13]))
        lok_Generatorspannung_max.append(float(letztexwerte[zeile][14]))
        lok_Leistung_Heiz_mittel.append(float(letztexwerte[zeile][15]))
        lok_Leistung_Heiz_min.append(float(letztexwerte[zeile][16]))
        lok_Leistung_Heiz_max.append(float(letztexwerte[zeile][17]))
    daten = [mitteln(lok_Einspeisestrom_mittel), min(lok_Einspeisestrom_min), max(lok_Einspeisestrom_max),
             mitteln(lok_Einspeiseleistung_mittel), min(lok_Einspeiseleistung_min), max(lok_Einspeiseleistung_max),
             mitteln(lok_Generatordrehzahl_mittel), min(lok_Generatordrehzahl_min), max(lok_Generatordrehzahl_max),
             mitteln(lok_Generatorspannung_mittel), min(lok_Generatorspannung_min), max(lok_Generatorspannung_max),
             mitteln(lok_Leistung_Heiz_mittel), min(lok_Leistung_Heiz_min), max(lok_Leistung_Heiz_max),]
    daten = listencheck(daten)
    return daten
# Verbindung mit Aeocon pruefen
def connection():
    port.close()
    port.open()
    kommando_ges='\x00\x06\x02\x01\x0b\x34\x00\x00\xb7'
    port.write(kommando_ges)
    read_string=port.read(11)
    if len(read_string)==11:
        return 1
    else:
        return 0

# Leert die Arrays
def arrays_leeren():
    aeocon.Einspeisestrom[:] = []
    aeocon.Einspeiseleistung[:] = []
    aeocon.Generatordrehzahl[:] = []
    aeocon.Generatorspannung[:] = []
    aeocon.Leistung_Heiz[:] = []

# Abfrage der Messdaten
def abfrage():
    """
    Abfragt die aktuelle Daten vom AEOCON, prueft auf die Plausibilitaet, speichert in Daten-Array
    """
    if connection():
        Einspeisestrom = I_Netz()
        Einspeiseleistung = P_Netz()
        Generatordrehzahl = n_WEA()
        Generatorspannung = U_WEA()
        Leistung_Heiz = P_Heiz()
        if (Einspeisestrom[0]<25)and(Einspeisestrom[0]>=0):
            aeocon.Einspeisestrom.append(float(Einspeisestrom[0]))
        else:
            aeocon.Einspeisestrom.append(float('nan'))
        if (Einspeiseleistung[0]<5000)and(Einspeiseleistung[0]>=0):
            aeocon.Einspeiseleistung.append(float(Einspeiseleistung[0]))
        else:
            aeocon.Einspeiseleistung.append(float('nan'))
        if (Generatordrehzahl[0]<500)and(Generatordrehzahl[0]>=0):
            aeocon.Generatordrehzahl.append(float(Generatordrehzahl[0]))
        else:
            aeocon.Generatordrehzahl.append(float('nan'))
        if (Generatorspannung[0]<500)and(Generatorspannung[0]>=0):
            aeocon.Generatorspannung.append(float(Generatorspannung[0]))
        else:
            aeocon.Generatorspannung.append(float('nan'))
        if (Leistung_Heiz[0]<10000)and(Leistung_Heiz[0]>=0):
            aeocon.Leistung_Heiz.append(float(Leistung_Heiz[0]))
        else:
            aeocon.Leistung_Heiz.append(float('nan'))
        daten=[float(Einspeisestrom[0]), float(Einspeiseleistung[0]), float(Generatordrehzahl[0]),
               float(Generatorspannung[0]), float(Leistung_Heiz[0])]              
    else:
        aeocon.Einspeisestrom.append(float('nan'))
        aeocon.Einspeiseleistung.append(float('nan'))
        aeocon.Generatordrehzahl.append(float('nan'))
        aeocon.Generatorspannung.append(float('nan'))
        aeocon.Leistung_Heiz.append(float('nan'))
        daten=[float('nan'), float('nan'), float('nan'), float('nan'), float('nan')]
    return daten

# Hier werden alle Wetterdaten gemittelt und die MinMax Werte gesucht
def zehn_minuten_mittel():
    daten = [mitteln(aeocon.Einspeisestrom), min(aeocon.Einspeisestrom), max(aeocon.Einspeisestrom),
             mitteln(aeocon.Einspeiseleistung), min(aeocon.Einspeiseleistung), max(aeocon.Einspeiseleistung),
             mitteln(aeocon.Generatordrehzahl), min(aeocon.Generatordrehzahl), max(aeocon.Generatordrehzahl),
             mitteln(aeocon.Generatorspannung), min(aeocon.Generatorspannung), max(aeocon.Generatorspannung),
             mitteln(aeocon.Leistung_Heiz), min(aeocon.Leistung_Heiz), max(aeocon.Leistung_Heiz)]
    daten = listencheck(daten)
    return daten

# Funktion zum mitteln einer 1-dimensionalen Liste aus floats
def mitteln(liste):
    anzahl_elemente = len(liste)
    try:
        mittel = 0
        gueltige_werte = 0
        for a in range(anzahl_elemente):
            if not math.isnan(liste[a]):
                mittel += liste[a]
                gueltige_werte += 1
        if gueltige_werte != 0:
            mittel /= gueltige_werte
        else:
            mittel = float('nan')
            logeintrag("Mitteln 1D Fehler: keine gueltigen Werte")
        return mittel
    except:
        logeintrag("Mitteln 1D Fehler: " + traceback.format_exc())
        return float('nan')

def logeintrag(nachricht):
    datei = open(pfad+file_log, "a")
    dt = datetime.now()
    dt = dt.strftime('%Y-%m-%d %H:%M:%S')
    nachricht = dt + " " + nachricht
    print nachricht
    nachricht += "\n"
    datei.write(nachricht)
    datei.close()    
#-------------------------------------------------------------------------------------------

def zeitabfrage():
    """
    Funktion die die Zeit ueberwacht und entsprechend andere Funktionen aufruft
    """
    sec = datetime.now().second
    minute = datetime.now().minute
    stunde = datetime.now().hour
    global sec_alt, minute_alt, stunde_alt
    if sec % 3 == 0 and sec != sec_alt:  # Alle drei Sekunden
        dreisekuendlich()
    if minute % 10 == 9 and minute != minute_alt:  # Alle zehn Minuten
        zehnminuetlich()
    if minute == 59 and minute != minute_alt:  # Jede Stunde
        stuendlich()
        if (stunde + 1) % 4 == 0:  # 1 Minute vor jeder 4. Stunde
            vierstuendlich()
        if stunde == 23:
            taeglich()  # Vor neuem Tag
    minute_alt = minute
    sec_alt = sec
    stunde_alt = stunde 

#-------------------------------------------------------------------------------------------
#Hauptfunktion main()
logeintrag("Skript Start")
while 1:
#for counter in range(1000):
    try:
        time.sleep(0.4) # Schlafen zur CPU Entlastung
        zeitabfrage()  # Hier werden je nach Zeit Funktionen aufgerufen
    except:
        logeintrag("Fehler: " + traceback.format_exc())
