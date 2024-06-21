import os
import time

def report_process():
    pipe_report = '/tmp/stat_to_report'                                                     # Pfad zur benannten Pipe für den Report-Prozess

                                                                                             # Versucht, die benannte Pipe exklusiv zu erstellen
    try:
        fifo_fd = os.open(pipe_report, os.O_RDWR | os.O_CREAT | os.O_EXCL)                   # Öffnet die benannte Pipe im Lese-Schreib-Modus und erstellt sie exklusiv
        os.close(fifo_fd)                                                                    # Schließt den Datei-Deskriptor sofort wieder
    except FileExistsError:                                                                  # Fängt den Fehler ab, wenn die benannte Pipe bereits existiert
        print(f"Named pipe '{pipe_report}' already exists.")                                 # Gibt eine Nachricht aus, dass die Pipe bereits existiert

    while True:                                                                              # Endlosschleife
        try:
            with open(pipe_report, 'r') as fifo_report:                                      # Öffnet die benannte Pipe im Lesemodus
                try:
                    tmp = fifo_report.readline()                                             # Liest eine Zeile aus der Pipe ein
                    #print(tmp, "Das haben wir aus der pipe zu report geholt.")
                    if not tmp:                                                              # Prüft, ob die Zeile leer ist
                        continue                                                             # Überspringt die Zeile falls sie leer sein sollte
                except BlockingIOError:                                                      # Fängt den Fehler ab, wenn die Pipe blockiert ist
                    print("FIFO empty")                                                      # Gibt eine Nachricht aus, dass die Pipe leer ist
                    continue                                                                 # Überspringt den Rest des Schleifendurchlaufs

                daten = tmp.strip()                                                          # Entfernt Leerzeichen am Anfang und Ende der Zeichenkette
                if daten:                                                                    # Prüft, ob 'daten' nicht leer ist
                  # print(daten, "daten aus der pipe im prozess report")
                    try:
                        summenwert, durchschnitt = map(float, daten.split(','))              # Wandelt die Werte in der Zeile 'daten' in Gleitkommazahlen um und teilt sie Summenwert und Durchschnitt zu
                        print(f"Report: Summe = {summenwert}   Mittelwert = {durchschnitt}") # Gibt die Summe und den Durchschnitt auf der Konsole aus
                    except ValueError as e:                                                  # Fängt Fehler ab, wenn die Werte in 'daten' nicht in Gleitkommazahlen umgewandelt werden können
                        print(f"ValueError: {e}. Data received: {daten}")                    # Gibt eine Fehlermeldung aus, falls ein Fehler auftritt, und zeigt die empfangenen Daten an
        except Exception as e:                                                               # Fängt alle anderen möglichen Ausnahmen ab
            print(f"Error reading from pipe: {e}")                                           # Gibt eine Fehlermeldung aus, falls ein Fehler beim Lesen der Pipe auftritt

        time.sleep(1)                                                                        # Erstellt eine Zeitverzögerung von einer Sekunde

if __name__ == "__main__":
    report_process()