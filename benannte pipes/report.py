import os
import time

def report_process():
    pipe_report = '/tmp/stat_to_report'  # Pfad zur benannten Pipe für den Report-Prozess

    # Versucht, die benannte Pipe exklusiv zu erstellen
    try:
        fifo_fd = os.open(pipe_report, os.O_RDWR | os.O_CREAT | os.O_EXCL)
        os.close(fifo_fd)  # Schließt den Datei-Deskriptor sofort wieder
    except FileExistsError:
        print(f"Named pipe '{pipe_report}' already exists.")

    while True:  # Endlosschleife
        try:
            with open(pipe_report, 'r') as fifo_report:  # Öffnet die benannte Pipe im Lesemodus
                try:
                    tmp = fifo_report.readline()
                    #print(tmp, "Das haben wir aus der pipe zu report geholt.")
                    if not tmp:
                        continue  # Skip if the line is empty
                except BlockingIOError:
                    print("FIFO empty")
                    continue

                daten = tmp.strip()  # Entfernt Leerzeichen am Anfang und Ende der Zeichenkette
                if daten:  # Prüft, ob 'daten' nicht leer ist
                  #  print(daten, "daten aus der pipe im prozess report")
                    try:
                        summenwert, durchschnitt = map(float, daten.split(','))  # Wandelt die Werte in der Zeile 'daten' in Gleitkommazahlen um
                        print(f"Report: Summe = {summenwert}, Mittelwert = {durchschnitt}")  # Gibt die Summe und den Durchschnitt auf der Konsole aus
                    except ValueError as e:  # Fängt Fehler ab, wenn die Werte in 'daten' nicht in Gleitkommazahlen umgewandelt werden können
                        print(f"ValueError: {e}. Data received: {daten}")  # Gibt eine Fehlermeldung aus, falls ein Fehler auftritt, und zeigt die empfangenen Daten an
        except Exception as e:  # Fängt alle anderen möglichen Ausnahmen ab
            print(f"Error reading from pipe: {e}")  # Gibt eine Fehlermeldung aus, falls ein Fehler beim Lesen der Pipe auftritt

        time.sleep(1)  # Erstellt eine Zeitverzögerung von einer Sekunde

if __name__ == "__main__":
    report_process()