import os
import time
import signal
import sys

#Kann: Erstellt mittels Fork 2 Kindprozesse
#Signal Handler Work in Progress (!!!)

child_pids = [] #Array für SignalHandler

def endlosprozess(process_number): #Ausgabe für Status
    while True: 
        print("Prozess ",process_number," läuft...")
        time.sleep(2)

def signal_handler(sig, frame):     #SIGNAL HANDLER Work in Progress
    print("Signal zum Beenden empfangen")
    for pid in child_pids:
        os.kill(pid, signal.SIGTERM)
    print("Alle Kindprozesse wurden beendet")
    sys.exit(0)

if __name__ == "__main__":                  #führt fork durch

    signal.signal(signal.SIGINT, signal_handler)    #AUfruf usw SignalHandler

    for i in range (2):                     #Erstellt 2 Prozesse
        #PID = Rückgabewert bei fork
        # -1 = fehlgeschlagen
        #  0 = Ich bin ein Kindprozess
        # >0 = Ich bin ein Elternprozess

        pid = os.fork()         #(Main1)Fork um Kindprozess zu erstellen mit Rückgabewert=pid

        if pid == 0:            #Startet NUR im KINDPROZESS, wegen pid=0
            endlosprozess(i+1)  #Aufruf Endlos_Status_Schleife wird gestartet
            os._exit(0)         #beendet Prozess??

        elif pid > 0:                   #(Main)Gibt Status aus
            print("Kindprozess ",i+1," mit PID ",pid," gestartet")

    