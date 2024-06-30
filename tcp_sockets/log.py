#enthält server der random zahlen empfängt und in log.txt schreibt

import socket   #für erstellung der sockets
import signal    #Importiert das Modul für Signalverarbeitung
import sys      #Importiert das Modul zur Interaktion mit dem Interpreter

HOST = "localhost" 
LOG_PORT = 5002

#Initialisierung der Sockets und der Variable shutting_down
log_socket = None         #zum sicherstellen, dass er im globalen Namensraum existiert
shutting_down = False       #programm ist nicht im prozess des runterfahrens

# Log-Prozess: Schreibt Messwerte in eine lokale Datei
def log_process():
     global log_socket       #global um zugriff auch innerhalb der anderen Dateien zu gewährleisten
     try:
        log_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #hey ich existiere
        log_socket.bind((HOST, LOG_PORT))   #hey auf dem port hab ich mich gebunden und bin da
        log_socket.listen(1)    #hey ich höre jetzt auch anderen zu
        print(f"Server listening on {HOST}:{LOG_PORT}")
        conn, addr = log_socket.accept()   #hey ich seh dich jetzt und aktzeptiere dich
    
   
        buffer = b''  #buffer zum sammeln aller Daten, da bei tcp sockets oft daten in teilen empfangen werden
        with open("log.txt", "a") as log: #Öffnet die Datei zum Anhängen und Dateizeiger ans Ende der Datei (Anhangsmodus)
       
         while True: #mindestens eine vollständige Nachricht im Buffer ist (endet mit \n)
            
            data = conn.recv(1024)  # Empfange bis zu 1024 Bytes 
            #fehler abfangen
            if not data:
                    print("not data")   #falls falsche oder unvollständige daten empfangen werden
                    break       #Verbindung schließen
            buffer += data
            while b'\n' in buffer:  # Verarbeite alle vollständigen Nachrichten im Puffer
             line, buffer = buffer.split(b'\n', 1)   #extrahiert diese vollständige Nachricht bis zum ersten \n 
                                                     #und lässt den Rest der Daten im Buffer
                                                     
             measuredValue = int(line.decode('utf-8'))  # Wandle die empfangenen Bytes in einen String und dann in einen Integer um
             log.write(f"Der Messwert ist: {measuredValue}\n")       #Schreibt den Wert in die Datei
             log.flush()  # Stellt sicher dass die Daten direkt aufgeschrieben werden

     #fehler abfangen        
     except Exception as e:
        print(f"An error occurred: {e}")
     finally:
        if log_socket:
            log_socket.close()      #Schließen des Sockets, falls geöffnet

#Signal handler zum beenden des Programms und schließen der Sockets
def signal_handler(sig, frame):
    global shutting_down        #global, damit der signal handler sie global deklarieren kann, obwohl sie außerhalb definiert ist
    if not shutting_down:           #stellt sicher das folgender code nur ausgefürt ist, falls nicht vorher schon shutting_down läuft
        shutting_down = True         #hier wird nun das programm auf runterfahren gestellt
         #schließt socket falls er existiert
        if log_socket:
            log_socket.close()
        sys.exit(0)         #beendet das Programm und gibt alle offenen Ressourcen frei

#Registrieren des signal handlers
signal.signal(signal.SIGINT, signal_handler)        #interrupt signal wird gesendet wenn strg+c gedrückt wird
signal.signal(signal.SIGTERM, signal_handler)          #terminate signal wird verwendet um programm zu beenden
        
#damit wir den log_process auch in der main starten können
if __name__ == '__main__':
    log_process()