import os
import time

def stat_process():
    pipe_stat = '/tmp/conv_to_stat'      # Pfad zur benannten Pipe für den Stat-Prozess
    pipe_report = '/tmp/stat_to_report'  # Pfad zur benannten Pipe für den Report-Prozess
    
    if not os.path.exists(pipe_stat):
        os.mkfifo(pipe_stat)
    if not os.path.exists(pipe_report):
        os.mkfifo(pipe_report)
    
    summenwert = 0
    anzahl = 0

    while True:
        try:
            with open(pipe_stat, 'r') as fifo_stat, open(pipe_report, 'w') as fifo_report:
                value = fifo_stat.readline().strip()  # Liest eine Zeile aus der fifo_stat Pipe und entfernt Leerzeichen und Zeilenumbrüche
                if value:
                    try:
                        zahl = float(value)  # Versucht, den gelesenen Wert in eine Gleitkommazahl umzuwandeln
                        summenwert += zahl  # Addiert den gelesenen Wert zur Summe summenwert
                        anzahl += 1  # Erhöht die Anzahl der gelesenen Werte, um den Durchschnitt zu berechnen
                        durchschnitt = summenwert / anzahl if anzahl > 0 else 0  # Berechnet den Durchschnitt aus der Summe und der Anzahl, wenn Anzahl > 0, sonst 0
                        fifo_report.write(f"{summenwert}\n{durchschnitt}\n")  # Schreibt die berechnete Summe und den Durchschnitt in die Pipe fifo_report
                        fifo_report.flush()  # Stellt sicher, dass die Daten sofort in die Pipe geschrieben werden
                    except ValueError as e:
                        print(f"ValueError: {e}. Data received: {value}")  # Gibt eine Fehlermeldung aus, wenn die Umwandlung in float fehlschlägt
        except OSError as e:
            print(f"Error reading from or writing to pipe: {e}")  # Gibt eine Fehlermeldung aus, wenn ein OSError beim Lesen oder Schreiben in die Pipes auftritt

        time.sleep(1)  # Wartet 1 Sekunde, bevor die Schleife erneut durchlaufen wird

    #fifo_stat.close()  # Diese Zeile sollte nicht hier sein, da die Pipes in den with-Statements geöffnet und geschlossen werden

if __name__ == "__main__":
    stat_process()