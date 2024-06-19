import os
import time
 
def report_process():
    pipe_report = '/tmp/stat_to_report'  # Pfad zur benannten Pipe für den Report-Prozess
    
    if not os.path.exists(pipe_report):
        os.mkfifo(pipe_report)

    while True:                                   # Endlosschleife
        try:
            with open(pipe_report, 'r') as fifo_report:  # Öffnet die benannte Pipe im Lesemodus
                daten = fifo_report.readlines()          # Liest alle Zeilen aus der Pipe und speichert sie in der Liste 'daten'
                if daten:                                # Prüft, ob 'daten' nicht leer ist
                    try:
                        summenwert, durchschnitt = map(float, daten)  # Wandelt die Werte in der Liste 'daten' in Gleitkommazahlen um und weist sie 'summenwert' und 'durchschnitt' zu
                        print(f"Report: Summe = {summenwert}, Mittelwert = {durchschnitt}")  # Gibt die Summe und den Durchschnitt auf der Konsole aus
                    except ValueError as e:  # Fängt Fehler ab, wenn die Werte in 'daten' nicht in Gleitkommazahlen umgewandelt werden können
                        print(f"ValueError: {e}. Data received: {daten}")  # Gibt eine Fehlermeldung aus, falls ein Fehler auftritt, und zeigt die empfangenen Daten an
        except Exception as e:  # Fängt alle anderen möglichen Ausnahmen ab
            print(f"Error reading from pipe: {e}")  # Gibt eine Fehlermeldung aus, falls ein Fehler beim Lesen der Pipe auftritt
       
        time.sleep(1)    # Erstellt eine Zeitversögerung von einer Sekunde

if __name__ == "__main__":
    report_process()