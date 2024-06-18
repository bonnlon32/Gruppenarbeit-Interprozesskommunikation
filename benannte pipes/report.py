import os
import time
 
def report_process():
        pipe_report = '/tmp/stat_to_report'  # Pfad zur benannten Pipe für den Report-Prozess
        
        while True:                                   # Endlosschleife
         with open(pipe_report, 'r') as fifo_report:  # Öffnet die benannte Pipe zum lesen
            daten = fifo_report.readlines()           # Liest alle Werte auf der Pipe aus und speichert sie in der Liste daten
            if daten:                                 # Prüft, dass die Liste nciht leer ist
                summenwert, durchschnitt = map(float, daten) # Hier werden die eingelesenen Zahlen in Gleitkommazahlen umgewandelt und sie werden Summenwert und Durchschnitt zugewiesen
                print(f"Report: Summe = {summenwert}, Mittelwert = {durchschnitt}") # Gibt die Summe und den Durchschnitt auf der Konsole aus

        time.sleep(1)    # Erstellt eine Zeitversögerung von eienr Sekunde

if __name__ == "__main__":
    report_process()