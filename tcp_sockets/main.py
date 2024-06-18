# #starten des gesamten prozesses
# #fork noch einbauen - als kommandozeileneingabe oder fork als duplizieren der prozesse?
# #signalhandler sigint noch einbauen
# #fehlerhafte kommandozeilen eingaben abfangen!!

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

#  '# Erstellen und Starten der Prozesse
# from multiprocessing import Process  # Modul zum Erstellen und Verwalten von Prozessen

# from conv import conv_process          # Importiert die Funktion für den A/D-Wandler-Prozess aus der conv Datei
# from log import log_process            # Importiert die Funktion für den Log-Prozess aus der log Datei
# from stats import stat_process         # Importiert die Funktion für den Stat-Prozess aus der stat Datei
# from report import report_process      # Importiert die Funktion für den Report-Prozess aus der report Datei


# def main():
#     processes = [
#         Process(target=conv_process),   # Erstellen des Prozesses für conv_process
#         Process(target=log_process),    # Erstellen des Prozesses für log_process
#         Process(target=stat_process),   # Erstellen des Prozesses für stat_process
#         Process(target=report_process)  # Erstellen des Prozesses für report_process
#     ]

    
#     for p in processes:
#         p.start()  # Startet jeden Prozess
    
#     for p in processes:
#         p.join()  # Wartet, bis jeder Prozess beendet ist

# if __name__ == "__main__": # Überprüft, ob das Skript direkt ausgeführt wird
#     main()                 # Ruft die Hauptfunktion auf
