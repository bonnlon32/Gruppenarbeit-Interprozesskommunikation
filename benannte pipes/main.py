import os
import signal  # Modul für das Behandeln von Signalen wie SIGINT (Ctrl+C)
import sys     # Modul zur Systemmanipulation (z.B. zum Beenden des Programms)
import time    # Modul zur Zeitsteuerung

from conv import conv_process         # Importiert die Funktion für den A/D-Wandler-Prozess aus der conv Datei
from log import log_process           # Importiert die Funktion für den Log-Prozess aus der log Datei
from stat_process import stat_process # Importiert die Funktion für den Stat-Prozess aus der stat Datei
from report import report_process     # Importiert die Funktion für den Report-Prozess aus der report Datei

pipe_conv_to_log = '/tmp/conv_to_log'        # Der Pfad für die benannten Pipe für den Log-Prozess
pipe_conv_to_stat = '/tmp/conv_to_stat'      # Der Pfad für die benannten Pipe für den Stat-Prozess
pipe_stat_to_report = '/tmp/stat_to_report'  # Der Pfad für die benannten Pipe für den Report-Prozess

# Signalhandler für SIGINT implementieren (Ctrl+C)
def signal_handler(sig, frame):
    print("Abbruchsignal empfangen. Prozesse werden beendet...") # Wird ausgegeben
    clean()      # Aufruf der Cleanup-Funktion
    sys.exit(0)  # Beendet das Programm

# Clean-Funktion erstellen, damit beim Beenden die Pipes entfernt werden
def clean():
    for pipe in [pipe_conv_to_log, pipe_conv_to_stat, pipe_stat_to_report]: # speichert alle drei Pipes in 'pipe'
        try:
            if os.path.exists(pipe):  # Überprüft, ob die Pipe existiert
               os.unlink(pipe)        # Entfernt die Pipe
        except FileNotFoundError: 
            pass                      # Wenn die Datei nicht gefunden wird, wird die Ausnahme ignoriert

def start_process(target_func):
    pid = os.fork()  # Erstellt einen neuen Prozess durch Aufteilen des aktuellen Prozesses in zwei Prozesse (Eltern- und Kindprozess)
    if pid == 0:  # Überprüft, ob dies der Kindprozess ist (pid == 0 bedeutet Kindprozess)
        target_func()  # Führt die Ziel-Funktion im Kindprozess aus
        os._exit(0)  # Beendet den Kindprozess nach Abschluss der Funktion
    else:
        return pid  # Gibt die Prozess-ID (pid) des Kindprozesses an den Elternprozess zurück

def main():
    # Erstellt die benannten Pipes, wenn sie nicht existieren
    for pipe in [pipe_conv_to_log, pipe_conv_to_stat, pipe_stat_to_report]: # Die drei Pipes werden in 'pipe' gespeichert
        if not os.path.exists(pipe):  # Überprüft, ob die Pipe nicht existiert
            os.mkfifo(pipe)           # Erstellt die Pipe

    # Erstellen und Starten der Prozesse
    processes = [ # Liste aus den vier Prozessen
        start_process(conv_process),   # Erstellen und Starten des Prozesses für conv_process
        start_process(log_process),    # Erstellen und Starten des Prozesses für log_process
        start_process(stat_process),   # Erstellen und Starten des Prozesses für stat_process
        start_process(report_process)  # Erstellen und Starten des Prozesses für report_process
    ]
    
    try:
        # Auf jeden Prozess warten, bis er beendet ist
        for pid in processes: 
            os.waitpid(pid, 0)           # Wartet, bis der Prozess mit der angegebenen Prozess-ID beendet ist
    except KeyboardInterrupt:  # Wenn der Benutzer `Ctrl+C` drückt, unterbrich das Programm
        print("Programm wurde unterbrochen. Prozesse werden beendet...") 
        clean()       # Führt die clean-Funktion aus
        sys.exit(0)   # Beendet das Programm mit einem Erfolgscode (0 steht für erfolgreichen Abschluss)

if __name__ == "__main__": # Überprüft, ob das Skript direkt ausgeführt wird
    signal.signal(signal.SIGINT, signal_handler) # Registriert einen Signalhandler für SIGINT (Ctrl+C), um das Programm zu beenden
    main()                 # Ruft die Hauptfunktion auf