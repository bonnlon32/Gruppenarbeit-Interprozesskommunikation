#enthält server der random zahlen empfängt und in log.txt schreibt
import socket
import signal
import sys

HOST = "localhost" 
LOG_PORT = 5002


log_socket = None
shutting_down = False

# Log-Prozess: Schreibt Messwerte in eine lokale Datei
def log_process():
     global log_socket
     try:
        log_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #hey ich existiere
        log_socket.bind((HOST, LOG_PORT))   #hey auf dem port bin ich
        log_socket.listen(1)    #hey ich höre jetzt auch anderen zu
        print(f"Server listening on {HOST}:{LOG_PORT}")
        conn, addr = log_socket.accept()   #hey ich seh dich jetzt
    
   
        buffer = b''  #buffer zum sammeln aller Daten, da bei tcp sockets oft daten in teilen empfangen werden
        with open("log.txt", "a") as log: #Öffnet die Datei zum Anhängen und Dateizeiger ans Ende der Datei (Anhangsmodus)
       
         while True: #mindestens eine vollständige Nachricht im Buffer ist (endet mit \n)
            
            data = conn.recv(1024)  # Empfange bis zu 1024 Bytes 
            #fehler prävention
            if not data:
                    print("Keine Daten empfangen, Verbindung wird geschlossen.")
                    break
            buffer += data
            while b'\n' in buffer:  # Verarbeite alle vollständigen Nachrichten im Puffer
             line, buffer = buffer.split(b'\n', 1)   #extrahiert diese vollständige Nachricht bis zum ersten \n 
                                                     #und lässt den Rest der Daten im Buffer
                                                     
             measuredValue = int(line.decode('utf-8'))  # Wandle die empfangenen Bytes in einen String und dann in einen Integer um
             log.write(f"Der Messwert ist: {measuredValue}\n")
             log.flush()  # Stellt sicher dass die Daten direkt aufgeschrieben werden
             
     except Exception as e:
        print(f"An error occurred: {e}")
     finally:
        if log_socket:
            log_socket.close()

def signal_handler(sig, frame):
    global shutting_down
    if not shutting_down:
        shutting_down = True
        #print('Control-C received and program is closing...')
        if log_socket:
            log_socket.close()
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
        
#damit wir den log_process auch in der main starten können
if __name__ == '__main__':
    log_process()