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
    print("Abbruchsignal empfangen. Prozesse werden beendet...") # Wird ausgegeben
    clean()      # Aufruf der Cleanup-Funktion
    sys.exit(0)  # Beendet das Programm

# Clean-Funktion erstellen, damit beim beenden die Pipes entfernt werden
def clean():
    for pipe in [pipe_conv_to_log, pipe_conv_to_stat, pipe_stat_to_report]: # speichert alle drei Pipes in 'pipe'
        try:
            if os.path.exists(pipe):  # Überprüft, ob die Pipe existiert
               os.unlink(pipe)        # Entfernt die Pipe
        except FileNotFoundError: 
            pass                      # Wenn die Datei nicht gefunden wird, wird die Ausnahme ignoriert

def main():
    # Erstellt die benannten Pipes, wenn sie nicht existieren
    for pipe in [pipe_conv_to_log, pipe_conv_to_stat, pipe_stat_to_report]: # Die drei Pipes werden in 'pipe' gespeichert
        if not os.path.exists(pipe):  # Überprüft, ob die Pipe nicht existiert
            os.mkfifo(pipe)           # Erstellt die Pipe

    # Erstellen und Starten der Prozesse
    processes = [ # Liste aus den vier Prozessen
        Process(target=conv_process),   # Erstellen des Prozesses für conv_process
        Process(target=log_process),    # Erstellen des Prozesses für log_process
        Process(target=stat_process),   # Erstellen des Prozesses für stat_process
        Process(target=report_process)  # Erstellen des Prozesses für report_process
    ]
    
    for p in processes:
        p.start()  # Startet jeden Prozess
    
    try:
        # Auf jeden Prozess warten, bis er beendet ist
        for p in processes: 
            p.join()           # Blockiert die Ausführung, bis alle Prozesse abgeschlossen sind
    except KeyboardInterrupt:  # Wenn der Benutzer `Ctrl+C` drückt, unterbrich das Programm
        print("Programm wurde unterbrochen. Prozesse werden beendet...") 
        clean()       # Führt die clean-Funktion aus
        sys.exit(0)   # Beende das Programm mit einem Erfolgscode (0 steht für erfolgreichen Abschluss) 


if __name__ == "__main__": # Überprüft, ob das Skript direkt ausgeführt wird
    signal.signal(signal.SIGINT, signal_handler) # Registriere einen Signalhandler für SIGINT (Ctrl+C), um das Programm zu beenden
    main()                 # Ruft die Hauptfunktion auf