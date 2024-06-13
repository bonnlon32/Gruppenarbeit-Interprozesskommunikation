#enthält server der zuhört und von client aus conv daten bekommt
#schreibt daten in eine datei und speichert ab

import socket
import struct

HOST = '127.0.0.1'
LOG_PORT = 5002

# Log-Prozess: Schreibt Messwerte in eine lokale Datei
def log_process():
    log_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    log_socket.connect((HOST, LOG_PORT))
    print("Log-Prozess verbunden.")

    with open("log.txt", "a") as log: #Öffnet die Datei zum Anhängen und Dateizeiger ans Ende der Datei (Anhangsmodus)
        while True:
            data = log_socket.recv(4) #Anzahl der Bytes, die aus dem Socket gelesen werden sollen 
            if not data: #fehler prävention
                break
            messwert = struct.unpack(data) #in binäre form gewandelte daten werden wieder umgewandelt
            log.write("Der Messwert ist: " + {messwert} + "\n")
        