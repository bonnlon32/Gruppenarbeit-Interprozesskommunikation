import os  
import signal                        # Modul für das Behandeln von Signalen wie SIGINT (Ctrl+C)
import sys                           # Modul zur Systemmanipulation (z.B. zum Beenden des Programms)
from multiprocessing import Process  # Modul zum Erstellen und Verwalten von Prozessen

from conv import conv_process          # Importiert die Funktion für den A/D-Wandler-Prozess aus der conv Datei
from log import log_process            # Importiert die Funktion für den Log-Prozess aus der log Datei
from stat_process import stat_process  # Importiert die Funktion für den Stat-Prozess aus der stat Datei
from report import report_process      # Importiert die Funktion für den Report-Prozess aus der report Datei

pipe_conv_to_log = '/tmp/conv_to_log'        # Der Pfad für die benannten Pipe für den Log-Prozess
pipe_conv_to_stat = '/tmp/conv_to_stat'      # Der Pfad für die benannten Pipe für den Stat-Prozess
pipe_stat_to_report = '/tmp/stat_to_report'  # Der Pfad für die benannten Pipe für den Report-Prozess

# Signalhandler für SIGINT implementieren (Ctrl+C)
def signal_handler(sig, frame):
    print("Abbruchsignal empfangen. Prozesse werden beendet...")
    cleanup()  # Aufruf der Cleanup-Funktion
    sys.exit(0)  # Beendet das Programm

def main():
    pass    # pass ist ein Platzhalter für die spätere Hauptlogik des Programms

if __name__ == "__main__": # Überprüft, ob das Skript direkt ausgeführt wird
    main()                 # Ruft die Hauptfunktion auf