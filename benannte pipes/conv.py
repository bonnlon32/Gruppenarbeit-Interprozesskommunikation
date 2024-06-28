import os
import random
import time

                                                                                      # Funktion simuliert einen A/D-Wandler(Von Noah).
def analog_to_digital_converter():
    #Gibt zufälligen Eingangswert (double zwischen -1 bis 5 Volt) aus, um A/D-Converter mit einschließlich nicht plausiblen Werten zu simulieren
    digital_value = round(random.uniform(0.1, 5),2)   
    if digital_value < 0:                                                              # Prüfung des Messwerts auf Plausibilität
        digital_value = 0                                                              # wenn Messwert nicht plausibel, wird auf 0 gesetzt
    return digital_value


def conv_process():
     pipe_log = '/tmp/conv_to_log'                                                     # Pfad zur benannten Pipe für den Log-Prozess
     pipe_stat = '/tmp/conv_to_stat'                                                   # Pfad zur benannten Pipe für den Stat-Prozess
     
     if not os.path.exists(pipe_log):                                                  # Überprüft, ob die bannte Pipe schon existiert
        os.mkfifo(pipe_log)                                                            # Erstellt die benannte Pipe, wenn sie noch nicht existiert
     if not os.path.exists(pipe_stat):                                                 # Überprüft, ob die bannte Pipe schon existiert
        os.mkfifo(pipe_stat)                                                           # Erstellt die benannte Pipe, wenn sie noch nicht existiert

     while True:    
         value = analog_to_digital_converter()                                         # Ruft die Funktion auf um den Wert in die pipes zu schreiben
         try:   
              with open(pipe_log, 'w') as fifo_log, open(pipe_stat, 'w') as fifo_stat: # Öffnet die Pipes zum Schreiben (w)                         # Endlosschleife erstellen
                   fifo_log.write(f"{value}\n")                                        # Schreibt die Zahl in die die Pipe mit einem Zeilenumbruch danach
                   fifo_log.flush()                                                    # Hiermit wird sichergestellt, dass die Zahl sofort in die Pipe geschrieben wird
                   fifo_stat.write(f"{value}\n")
                   fifo_stat.flush()
         except OSError as e:
               print(f"Error writing to pipe: {e}")
       
         time.sleep(1)                                                                 # Stellt sicher, dass es immer eine Sekunde wartet, bevor eine neue Zahlgeneriert und in die Pipe geschrieben wird

if __name__ == "__main__":
     
    # Startet den Conv-Prozess
    conv_process()