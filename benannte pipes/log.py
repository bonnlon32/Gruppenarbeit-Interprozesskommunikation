import os

# Erster Entwurf für den Log-Prozess. Hier werden die Zufallszahlen aus conv in eine Datei gespeichert.
def log_process():
     pipe_log = '/tmp/conv_to_log'  # Der Pfad zur benannten Pipe für den Log-Prozess
     log_file = 'log.txt'           # Datei, in die die Werte geschrieben werden
     
     fifo_log = open(pipe_log, 'r')   # Öffnet die Pipe zum auslesen
     log = open(log_file, 'a')        # Öffnet die Log-Datei zum schreiben

     while True:                              # Unendlichschleife erstellen
        value = fifo_log.readline().strip()   # liest eine Zeile aus der Pipe ein und speichert sie in value
        if value:                             # Prüft, dass die Zahl nicht null ist
            log.write(f"{value}\n")           # Schreibt die Zahl die im Moment in value gespeichert ist in der Datei und macht danach immer einen Zeilenumbruch
            log.flush()                       # Hiermit wird die Zahl sofort in die Datei geschrieben

     fifo_log.close()                         # Schließt die Pipe
     log.close()                              # Schließt die Datei

if __name__ == "__main__":
    log_process()