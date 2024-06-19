# # #starten des gesamten prozesses
# # #fork noch einbauen - als kommandozeileneingabe oder fork als duplizieren der prozesse?
# # #signalhandler sigint noch einbauen
# # #fehlerhafte kommandozeilen eingaben abfangen!!

# import sys
# import signal

# # Signalhandler für SIGINT
# #def signal_handler(sig, frame):
#     print("Programm wird beendet...")
#     sys.exit(0)

# # Registrieren des Signalhandlers für SIGINT
# signal.signal(signal.SIGINT, signal_handler)

# # Einfache Endlosschleife, um das Programm am Laufen zu halten
# while True:
#     pass


#fork
import os # Importiert das Betriebssystem-Modul, das für das Arbeiten mit Prozessen und Pfaden verwendet wird
import time # Importiert das Zeit-Modul, um Pausen und Wartezeiten zu ermöglichen


def start_process(script_path):
    pid = os.fork() # Erstellt einen neuen Prozess durch Aufteilen des aktuellen Prozesses in zwei Prozesse (Eltern- und Kindprozess)
    if pid == 0:  # Überprüft, ob dies der Kindprozess ist (pid == 0 bedeutet Kindprozess)
        os.execvp('python3', ['python3', script_path]) # Ersetzt das Kindprozess-Programm mit dem angegebenen Python-Skript
    else:
        return pid # Gibt die Prozess-ID (pid) des Kindprozesses an den Elternprozess zurück

if __name__ == '__main__':  # Überprüft, ob das Skript direkt ausgeführt wird (nicht importiert als Modul)
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Ermittelt das Verzeichnis, in dem sich das aktuelle Skript befindet
    scripts = ['log.py', 'stats.py', 'report.py']  # Listet die Namen der Skripte auf, die gestartet werden sollen
    processes = []  # Erstellt eine leere Liste, um die Prozess-IDs der gestarteten Skripte zu speichern

    for script in scripts:  # Schleife über jedes Skript in der scripts-Liste
        script_path = os.path.join(base_dir, script) # Erstellt den vollständigen Pfad zum Skript
        if os.path.isfile(script_path):  # Überprüft, ob das Skript existiert
            pid = start_process(script_path)  # Startet das Skript in einem neuen Prozess und erhält die Prozess-ID
            processes.append(pid)  # Fügt die Prozess-ID der Liste der Prozesse hinzu
        else:
            print(f"Error: {script_path} not found") # Gibt eine Fehlermeldung aus, wenn das Skript nicht gefunden wird


    # Wartezeit um sicherzustellen, dass alle Serverprozesse laufen
    time.sleep(3)

    # Starte conv.py Prozess
    conv_script = os.path.join(base_dir, 'conv.py')  # Erstellt den vollständigen Pfad zum 'conv.py'-Skript
    if os.path.isfile(conv_script): # Überprüft, ob das 'conv.py'-Skript existiert
        pid = start_process(conv_script)  # Startet 'conv.py' in einem neuen Prozess und erhält die Prozess-ID
        processes.append(pid)   # Fügt die Prozess-ID der Liste der Prozesse hinzu
    else:
        print(f"Error: {conv_script} not found") # Gibt eine Fehlermeldung aus, wenn 'conv.py' nicht gefunden wird

    # Optional, warte auf alle Prozesse
    for pid in processes:  # Schleife über jede Prozess-ID in der Prozesse-Liste
        os.waitpid(pid, 0) # Wartet, bis der Prozess mit der angegebenen Prozess-ID beendet ist

    print("All processes have finished.") 

