#server
import socket

HOST = "localhost" 
LOG_PORT = 5002


# Log-Prozess: Schreibt Messwerte in eine lokale Datei
def log_process():
    log_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #hey ich existiere
    log_socket.bind((HOST, LOG_PORT))   #hey auf dem port bin ich
    log_socket.listen(1)    #hey ich höre jetzt auch anderen zu
    print(f"Server listening on {HOST}:{LOG_PORT}")
    conn, addr = log_socket.accept()   #hey ich seh dich jetzt
    print(f"Verbindung von log zu {addr} hergestellt.")
   
    buffer = b''
    with open("log.txt", "a") as log: #Öffnet die Datei zum Anhängen und Dateizeiger ans Ende der Datei (Anhangsmodus)
        while True:
            print("In while true Teil von log gekommen")
            data = conn.recv(1024)  # Empfange bis zu 1024 Bytes 
            #fehler prävention
            if not data:
                    print("Keine Daten empfangen, Verbindung wird geschlossen.")
                    break
            buffer += data
            while b'\n' in buffer:  # Verarbeite alle vollständigen Nachrichten im Puffer
             line, buffer = buffer.split(b'\n', 1)
             measuredValue = int(line.decode('utf-8'))  # Wandle die empfangenen Bytes in einen String und dann in einen Integer um
             log.write(f"Der Messwert ist: {measuredValue}\n")
             log.flush()  # Stellt sicher dass die Daten direkt aufgeschrieben werden
             
if __name__ == '__main__':
    log_process()