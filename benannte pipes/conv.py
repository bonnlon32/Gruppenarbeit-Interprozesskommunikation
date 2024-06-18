import os
import random
import time
# Erster Entwurf für den Conv-Prozess. Hier werden Zufallszahlen generiert die später weiterverarbeitet werden

                                                   # Funktion simuliert einen A/D-Wandler(Von Noah).
def analog_to_digital_converter():
    analog_value = random.uniform(0, 5)            # Erzeugt einen zufälligen analogen Wert zwischen 0 und 5 Volt.
    digital_value = int((analog_value / 5) * 255)  # Konvertiert den analogen Wert in einen digitalen Wert (8-Bit-Auflösung).
    return digital_value


def conv_process():
     pipe_log = '/tmp/conv_to_log'    # Pfad zur benannten Pipe für den Log-Prozess
     pipe_stat = '/tmp/conv_to_stat'  # Pfad zur benannten Pipe für den Stat-Prozess
     
     if not os.path.exists(pipe_log):  # Überprüft, ob die bannte Pipe schon existiert
        os.mkfifo(pipe_log)            # Erstellt die benannte Pipe, wenn sie noch nicht existiert
     if not os.path.exists(pipe_stat): # Überprüft, ob die bannte Pipe schon existiert
        os.mkfifo(pipe_stat)           # Erstellt die benannte Pipe, wenn sie noch nicht existiert

     fifo_log = open(pipe_log, 'w')          # Öffnet die Pipes zum Schreiben (w)
     fifo_stat = open(pipe_stat, 'w')

     while True:                              # Endlosschleife erstellen
        value = analog_to_digital_converter()   # Ruft die Funktion auf um den Wert in die pipes zu schreiben
        fifo_log.write(f"{value}\n")            # Schreibt die Zahl in die die Pipe mit einem Zeilenumbruch danach
        fifo_log.flush()                        # Hiermit wird sichergestellt, dass die Zahl sofort in die Pipe geschrieben wird
        fifo_stat.write(f"{value}\n")
        fifo_stat.flush()
      
        time.sleep(1)                           # Stellt sicher, dass es immer eine Sekunde wartet, bevor eine neue Zahlgeneriert und in die Pipe geschrieben wird

     fifo_log.close()                        # Schließt die Pipes
     fifo_stat.close()

if __name__ == "__main__":
     
    # Startet den Conv-Prozess
    conv_process()