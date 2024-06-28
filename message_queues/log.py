import random
import os
import time

def log_process(mqToLog):
    
    print("- - - LOG-PROZESS\t GESTARTET - - -")

    filename = "random_numbers.txt"                     # Dateiname, in die die zufälligen Zahlen geschrieben werden sollen

    try:

        while True:                                     # Endlosschleife von Conv
            time.sleep(1)

            message, priorität = mqToLog.receive()      # Empfangen der Nachricht, speichern der Prio sepperat #(b'Zahl',0) b = bytes, String, priorität >> 0 = Standard
            message = message.decode()                  # Konvertierung von Byte
                              
            digital_num = message                       
            with open(filename, "a") as file:           # Öffnet Datei im Anhangmodus (a = append)
                file.write(f"{digital_num}\n")
            print(f"LOG Zufallswert: {digital_num}\t-> In die Datei '{filename}' geschrieben.") # Ausgabe
            
            time.sleep(1.5)

    except KeyboardInterrupt:
        pass