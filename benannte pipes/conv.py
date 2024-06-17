import os
import random
# Erster Entwurf für den Conv-Prozess. Hier werden Zufallszahlen generiert die später weiterverarbeitet werden

                                                   # Funktion simuliert einen A/D-Wandler(Von Noah).
def analog_to_digital_converter():
    analog_value = random.uniform(0, 5)            # Erzeugt einen zufälligen analogen Wert zwischen 0 und 5 Volt.
    digital_value = int((analog_value / 5) * 255)  # Konvertiert den analogen Wert in einen digitalen Wert (8-Bit-Auflösung).
    return digital_value
#kekse

def conv_process():
     pipe_log = '/tmp/conv_to_log'    # Pfad zur benannten Pipe für den Log-Prozess
     pipe_stat = '/tmp/conv_to_stat'  # Pfad zur benannten Pipe für den Stat-Prozess
     
     fifo_log = open(pipe_log, 'w')          # Öffnet die Pipes zum Schreiben (w)
     fifo_stat = open(pipe_stat, 'w')

     value = analog_to_digital_converter()   # Ruft die Funktion auf um den Wert in die pipes zu schreiben
 
     fifo_log.write(f"{value}\n")            # Schreibt die Zahl in die die Pipe mit einem Zeilenumbruch danach
     fifo_log.flush()                        # Hiermit wird sichergestellt, dass die Zahl sofort in die Pipe geschrieben wird

     fifo_stat.write(f"{value}\n")
     fifo_stat.flush()

     fifo_log.close()                        # Schließt die Pipes
     fifo_stat.close()

if __name__ == "__main__":
    # Startet den Conv-Prozess
    conv_process()