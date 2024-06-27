import os
import time
import signal
import sys

#importiert die Prozesse
from conv import conv_process
from log import log_process
from report import report_process
from stat_ import stat_process


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


    processes = [conv_process, log_process, report_process, stat_process] #Liste der Prozesse

    signal.signal(signal.SIGINT, signal_handler)    #Aufruf SignalHandler

    for i in range (len(processes)):            #Erstellt Kindprozesse mit Fork, bis alle gestartet sind
        #PID = Rückgabewert bei fork
        # -1 = fehlgeschlagen
        #  0 = Ich bin ein Kindprozess
        # >0 = Ich bin ein Elternprozess

        pid = os.fork()         #Fork um Kindprozess zu erstellen mit Rückgabewert=pid
                                #Eltern&Kindprozess läuft ab hier als identische Kopie weiter, außer dass pid Wert anders ist

        if pid == 0:            #Startet NUR im KINDPROZESS, wegen pid=0

            selected_process = processes[i]     #geht die Liste nacheinander durch, um die Prozesse zu starten
            selected_process()                  #startet Prozess

            #beendet Prozess wie sys.exit(), aber für Kindprozess
            os._exit(0)         #Code erreicht diese Stelle nur auf normalen Wege, wenn endlosprozess() enden würde

        elif pid > 0:                                               #Sollte nur in Elernprozess starten, da pid>0
            print("Kindprozess ",i+1," mit PID ",pid," gestartet")  #Gibt Status aus
            child_pids.append(pid)                                  #Speichert PID von Kindprozess in Array

        else:                               #Wenn Fork fehlschlägt (pid = -1)
            print("Fork für Kindprozess", i+1 ," Fehlgeschlagen")   
            sys.exit(1)                     #beendet Programm

    for _ in range(len(processes)):
        print("warte auf Beendung von Kindprozesse")
        os.wait()    