#enthält server der zuhört und zahlen von conv bekommt

#rechnet mittelwert und summe aus werten zsm 
#mittelwert wird float- schwierig zu übertragen, also umgehen
#wir das und übertragen als integer und basteln am ende wieder als 
#float zusammen

# enthält client der den mittelwert und summe an report schickt
    

#Beispiel - noch nicht an die Aufgabe angepasst - nur Grundidee

import socket
import struct

HOST = '127.0.0.1'
STAT_PORT = 5003

# Stat-Prozess: Berechnet Mittelwert und Summe der Messwerte
def stat_process():
    stat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    stat_socket.bind((HOST, STAT_PORT))
    stat_socket.listen(1)
    print("Stat-Prozess gestartet und wartet auf Verbindungen...")
    conn, addr = stat_socket.accept()
    print(f"Verbindung zu {addr} hergestellt.")

    summe = 0
    anzahl = 0

    while True:
        data = conn.recv(4) #nicht nur 4 byte weil float empfangen wird???
        if not data:
            break
        messwert = struct.unpack(data)
        summe += messwert
        anzahl += 1
        mittelwert = summe / anzahl
        conn.send(struct.pack(mittelwert))
        conn.send(struct.pack(summe))

