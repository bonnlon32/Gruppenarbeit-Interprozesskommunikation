#random zahl wird erstellt
#client schickt diese zahl an log und stat

#Beispiel - noch nicht an die Aufgabe angepasst - nur Grundidee
#mit server anfangen und nicht client!


import random #für random zahl
import time #für 1 sek abstände
import socket #für erstellung der sockets
import struct #um strings von bytes in und aus verschiedenen c-strukturen zu packen & zu entpacken

# Konstanten für Host und Ports (wohin?? hier rein oder main?)
HOST = '127.0.0.1'  #localhost adresse (lokal auf dem betriebssystem ohne das netzwerk zu verlassen)
CONV_PORT = 5001  #beliebige zahl, nur manche adressen sind reserviert

# Conv-Prozess: Generiert Zufallszahlen und sendet sie an Log und Stat
def conv_process():
    conv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conv_socket.bind((HOST, CONV_PORT))
    conv_socket.listen(1)
    print("Conv-Prozess gestartet und wartet auf Verbindungen...")
    conn, addr = conv_socket.accept()   # Adresse des Clients, der die Verbindung hergestellt hat, addr ein Tupel (client_ip, client_port).
    print(f"Verbindung zu {addr} hergestellt.")

    while True:
        messwert = random.randint(0, 100)  # Zufallszahl als Messwert
        conn.send(struct.pack('!I', messwert))  # Messwert senden
        time.sleep(1)  # Wartezeit zwischen den Messungen