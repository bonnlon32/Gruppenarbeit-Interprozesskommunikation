import os  
import signal  # Modul für das Behandeln von Signalen wie SIGINT (Ctrl+C)

# Erstes Gerüst für den Main-Prozess

from conv import conv_process          # Importiert die Funktion für den A/D-Wandler-Prozess aus der conv Datei
from log import log_process            # Importiert die Funktion für den Log-Prozess aus der log Datei
from stat_process import stat_process  # Importiert die Funktion für den Stat-Prozess aus der stat Datei
from report import report_process      # Importiert die Funktion für den Report-Prozess aus der report Datei

def main():
    pass    # pass ist ein Platzhalter für die spätere Hauptlogik des Programms

if __name__ == "__main__": # Überprüft, ob das Skript direkt ausgeführt wird
    main()                 # Ruft die Hauptfunktion auf