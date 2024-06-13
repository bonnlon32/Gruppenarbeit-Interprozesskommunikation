#client

import random #für random zahl
import time #für 1 sek abstände
import socket #für erstellung der sockets
import struct #um strings von bytes in und aus verschiedenen c-strukturen zu packen & zu entpacken

# Konstanten für Host und Ports (wohin?? hier rein oder main?)
HOST = "localhost" #localhost adresse (lokal auf dem betriebssystem ohne das netzwerk zu verlassen)
LOG_PORT = 5002
STAT_PORT = 5003  #beliebige zahl, nur manche adressen sind reserviert

# Conv-Prozess: Generiert Zufallszahlen und sendet sie an Log und Stat
def conv_process():

    #client erstellen und zu port verbinden
    log_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    stat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    log_socket.connect((HOST, LOG_PORT))
    stat_socket.connect((HOST, STAT_PORT))
    print(f"Verbindung zu Log und Stat hergestellt.")

    while True:
        messwert = random.randint(0, 10)  # Zufallszahl als Messwert
        # Messwert senden
        log_socket.sendall(struct.pack('!f', messwert))
        stat_socket.sendall(struct.pack('!f', messwert))

        time.sleep(1)  # Wartezeit zwischen den Messungen

if __name__ == '__main__':
    conv_process()