import time

# Dieser Endlosprozess empfängt Daten mittels MessageQueue aus Conv und speichert diese in einer Txt Datei

def log_process(mqToLog):
    time.sleep(1)

    filename = "random_numbers.txt"                     # Dateiname, in die die zufälligen Zahlen geschrieben werden sollen

    while True:                                     # Endlosschleife von Conv
        message, priority = mqToLog.receive()      # Empfangen der Nachricht, speichern der Prio sepperat, priorität: 0 = Standard
        digital_num = message.decode()              # Konvertierung von Byte                 

        with open(filename, "a") as file:           # Öffnet Datei im Anhangmodus (a = append)
            file.write(f"{digital_num}\n")          # Automatische Schließung nach Verlassen des Blocks
        
        time.sleep(0.5)