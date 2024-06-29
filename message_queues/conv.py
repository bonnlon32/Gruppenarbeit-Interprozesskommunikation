import time
import posix_ipc

# Dieser Endlosprozess empfängt Daten mittels MessageQueue aus Conv und speichert diese in einer Txt Datei

def log_process(mqToLog):
    time.sleep(1)
    print("- - - LOG-PROZESS\t GESTARTET - - -", flush=True)    # flush=True - verhindert Pufferung von Befehl - os.kill von Singalhandler ordentlich Prozess terminiert

    filename = "random_numbers.txt"                     # Dateiname, in die die zufälligen Zahlen geschrieben werden sollen

    try:

        while True:                                     # Endlosschleife von Conv


            message, priorität = mqToLog.receive()      # Empfangen der Nachricht, speichern der Prio sepperat #(b'Zahl',0) b = bytes, String, priorität >> 0 = Standard
            digital_num = message.decode()              # Konvertierung von Byte                 

            with open(filename, "a") as file:           # Öffnet Datei im Anhangmodus (a = append)
                file.write(f"{digital_num}\n")          # Automatische Schließung nach Verlassen des Blocks
            
            time.sleep(0.5)

    except KeyboardInterrupt:
        pass