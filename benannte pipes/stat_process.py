import os
import time

# Erster Entwurf für den Stat-Prozess. Hier wird mit den zuvor erzeugten Zufallszahlen Summe und Durchschnitt berechnet
def stat_process():
    pipe_stat = '/tmp/conv_to_stat'      # Pfad zur benannten Pipe für den Stat-Prozess
    pipe_report = '/tmp/stat_to_report'  # Pfad zur benannten Pipe für den Report-Prozess
    
    fifo_stat = open(pipe_stat, 'r')     # Pipe öffnen
    
    summenwert = 0
    anzahl = 0

    while True:                                # Endlosschleife 
        zeile = fifo_stat.readline().strip()   # Hier wird eine Zeile aus der benannten Pipe eingelesen
        if zeile:
            zahl = int(zeile)                  # Die eingelesene Zahl wird in einen int umgewandelt
            summenwert = summenwert + zahl
            anzahl = anzahl + 1                # Anzahl um den Durchschnitt zu berechnen
  
        durchschnitt = summenwert / anzahl if anzahl > 0 else 0 # Durchschnitt aus Anzahl und Summe berechnen


        with open(pipe_report, 'w') as fifo_report:                       # Pipe zu Report öffnen
                fifo_report.write(f"{summenwert}\n{durchschnitt}\n")  # Die Summe und den Durchschnitt in die Pipe schreiben

    time.sleep(1)

    fifo_stat.close()                          #Pipe wird geschlossen

if __name__ == "__main__":
    stat_process()