#enthält signal handler und fork um alle Prozesse gleichzeitig zu starten

import os # Importiert das Betriebssystem-Modul, das für das Arbeiten mit Prozessen und Pfaden verwendet wird
import time # Importiert das Zeit-Modul, um Pausen und Wartezeiten zu ermöglichen
import signal
import sys

# Signal-Handler-Funktion
def signal_handler(sig, frame):
    print('Control-C received and program is closing...')
    for pid in processes:
        os.kill(pid, signal.SIGTERM)
    sys.exit(0)

# Signal-Handler registrieren
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def start_process(script_path):
    pid = os.fork() # Erstellt neuen Prozess durch Aufteilen des aktuellen Prozesses in zwei Prozesse (Eltern- und Kindprozess)
    if pid == 0:  # Überprüft, ob dies der Kindprozess ist (pid == 0 bedeutet Kindprozess)
        os.execvp('python3', ['python3', script_path]) # Ersetzt Kindprozess-Programm mit dem angegebenen Python-Skript
    else:
        return pid # Gibt Prozess-ID (pid) des Kindprozesses an den Elternprozess zurück

if __name__ == '__main__':  # Überprüft, ob Skript direkt ausgeführt wird 
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Ermittelt das Verzeichnis, in dem sich das aktuelle Skript befindet
    scripts = ['log.py', 'stats.py', 'report.py']  # Listet Namen der Skripte auf, die gestartet werden sollen
    processes = []  # Erstellt leere Liste, um Prozess-IDs der gestarteten Skripte zu speichern

    for script in scripts:  # Schleife über jedes Skript in der scripts-Liste
        script_path = os.path.join(base_dir, script) # Erstellt vollständigen Pfad zum Skript
        if os.path.isfile(script_path):  # Überprüft, ob das Skript existiert
            pid = start_process(script_path)  # Startet Skript in einem neuen Prozess und erhält die Prozess-ID
            processes.append(pid)  # Fügt Prozess-ID der Liste der Prozesse hinzu
        else:
            print(f"Error: {script_path} not found") # Gibt Fehlermeldung aus, wenn das Skript nicht gefunden wird


    # Wartezeit um sicherzustellen, dass alle Serverprozesse laufen
    time.sleep(3)

    # Starte conv.py Prozess
    conv_script = os.path.join(base_dir, 'conv.py')  # Erstellt vollständigen Pfad zum 'conv.py'-Skript
    if os.path.isfile(conv_script): # Überprüft, ob das 'conv.py'-Skript existiert
        pid = start_process(conv_script)  # Startet 'conv.py' in einem neuen Prozess und erhält Prozess-ID
        processes.append(pid)   # Fügt Prozess-ID der Liste der Prozesse hinzu
    else:
        print(f"Error: {conv_script} not found") # Gibt Fehlermeldung aus, wenn 'conv.py' nicht gefunden wird

      # Warte auf alle Prozesse
    try:
        for pid in processes:
            os.waitpid(pid, 0)
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)
   

