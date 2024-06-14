import os

# Erster Entwurf für den Log-Prozess. Hier werden die Zufallszahlen aus conv in eine Datei gespeichert.
def log_process():
     pipe_log = '/tmp/conv_to_log'  # Der Pfad zur benannten Pipe für den Log-Prozess
     log_file = 'log.txt'  # Datei, in die die Werte geschrieben werden
     
     fifo_log = open(pipe_log, 'r')   #Öffnet die Pipe zum auslesen
     log = open(log_file, 'a')        #Öffnet die Log-Datei zum schreiben

     pass

if __name__ == "__main__":
    log_process()