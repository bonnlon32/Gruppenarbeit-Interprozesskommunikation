import os
import time
import signal
import sys

child_pids = [] #Array um alle PIDs der Kindprozesse zu speichern -> für SignalHandler

def endlosprozess(process_number): #Ausgabe für Status vom Kindprozess initialisiert
    while True: 
        print("Prozess ",process_number," läuft...")
        time.sleep(2)

def signal_handler(sig, frame):                 #Signal Handler für Ctrl + C Interrupt
    print("Signal zum Beenden empfangen")
    for pid in child_pids:
        os.kill(pid, signal.SIGTERM)            #Sendet SIGTERM an jeden Kindprozess
    print("Alle Kindprozesse wurden beendet")
    sys.exit(0)                                 # beendet main

if __name__ == "__main__":                  

    anzahlProzesse = 2      #Wie viele Kindprozesse gestartet werden sollen

    signal.signal(signal.SIGINT, signal_handler)    #Aufruf SignalHandler

    for i in range (anzahlProzesse):                #Erstellt Kindprozesse mit Fork
        #PID = Rückgabewert bei fork
        # -1 = fehlgeschlagen
        #  0 = Ich bin ein Kindprozess
        # >0 = Ich bin ein Elternprozess

        pid = os.fork()         #(Main)Fork um Kindprozess zu erstellen mit Rückgabewert=pid

        if pid == 0:            #Startet NUR im KINDPROZESS, wegen pid=0
            endlosprozess(i+1)  #Aufruf Endlos_Status_Schleife wird gestartet und läuft erstmal endlos
            #beendet Prozess wie sys.exit(), aber für Kindprozess
            os._exit(0)         #Code erreicht diese Stelle nur auf normalen Wege, wenn endlosprozess() enden würde

        elif pid > 0:                                               #Sollte nur in Elernprozess starten, da pid>0
            print("Kindprozess ",i+1," mit PID ",pid," gestartet")  #Gibt Status aus
            child_pids.append(pid)                                  #Speichert PID von Kindprozess in Array

        else:                               #Wenn Fork fehlschlägt (pid = -1)
            print("Fork Fehlgeschlagen")   
            sys.exit(1)                     #beendet Programm

    for _ in range(anzahlProzesse):
        os.wait()                       #wartet bis alle Kindprozesse geendet sind, damit signalHandler funktioniert und main weiter läuft