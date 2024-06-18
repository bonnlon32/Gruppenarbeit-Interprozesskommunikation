#server
import socket
import struct

HOST = "localhost" 
LOG_PORT = 5002


# Log-Prozess: Schreibt Messwerte in eine lokale Datei
def log_process():
    log_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #hey ich existiere
    log_socket.bind((HOST, LOG_PORT))   #hey auf dem port bin ich
    log_socket.listen(1)    #hey ich höre jetzt auch anderen zu
    print(f"Server listening on {HOST}:{LOG_PORT}")
    conn, addr = log_socket.accept()   #hey ich seh dich jetzt
    print(f"Verbindung zu {addr} hergestellt.")
   

    with open("log.txt", "a") as log: #Öffnet die Datei zum Anhängen und Dateizeiger ans Ende der Datei (Anhangsmodus)
        while True:
            data = conn.recv(4) #Anzahl der Bytes, die aus dem Socket gelesen werden sollen 
            if not data: #fehler prävention
                break
            measuredValue = struct.unpack('!I', data)  #in binäre form gewandelte daten werden wieder umgewandelt
            log.write("Der Messwert ist: " + str(measuredValue[0]) + "\n")

if __name__ == '__main__':
    log_process()