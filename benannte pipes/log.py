import os
import time

def log_process():
     pipe_log = '/tmp/conv_to_log'  # Der Pfad zur benannten Pipe für den Log-Prozess
     log_file = 'log.txt'           # Datei, in die die Werte geschrieben werden
     
     if not os.path.exists(pipe_log): # Überprüft, ob die benannte Pipe existiert, wenn nicht:
        os.mkfifo(pipe_log)           # wird hiermit die benannte Pipe erstellt

     fifo_log = open(pipe_log, 'r')   # Öffnet die Pipe zum auslesen
     log = open(log_file, 'a')        # Öffnet die Log-Datei zum schreiben

     while True:                              # Unendlichschleife erstellen
        value = fifo_log.readline().strip()   # liest eine Zeile aus der Pipe ein und speichert sie in value
        if value:                             # Prüft, dass die Zahl nicht null ist
            log.write(f"{value}\n")           # Schreibt die Zahl die im Moment in value gespeichert ist in der Datei und macht danach immer einen Zeilenumbruch   
            log.flush()                       # Hiermit wird die Zahl sofort in die Datei geschrieben
        
        time.sleep(1)                         # Stellt sicher, dass es immer eine Sekunde wartet, bevor die nächste Zahl in die Pipe geschrieben wird

     fifo_log.close()                         # Schließt die Pipe
     log.close()                              # Schließt die Datei

if __name__ == "__main__":
    log_process()