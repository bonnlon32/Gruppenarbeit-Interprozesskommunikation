import os

# Erster Entwurf für den Stat-Prozess. Hier wird mit den zuvor erzeugten Zufallszahlen Summe und Durchschnitt berechnet
def stat_process():
    pipe_stat = '/tmp/conv_to_stat'  # Pfad zur benannten Pipe für den Stat-Prozess
    pipe_report = '/tmp/stat_to_report'  # Pfad zur benannten Pipe für den Report-Prozess
    
    fifo_stat = open(pipe_stat, 'r')     # Pipe öffnen
    
    summenwert = 0
    anzahl = 0

if __name__ == "__main__":
    stat_process()