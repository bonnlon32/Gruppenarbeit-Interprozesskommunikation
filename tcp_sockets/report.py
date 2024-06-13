#enthält server der stat zuhört und mittelwert und summe bekommt
#gibt daten in shell aus

import socket
import struct
import time

HOST = '127.0.0.1'
STAT_PORT = 5003

# Report-Prozess: Gibt die statistischen Daten in der Shell aus
def report_process():
    report_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    report_socket.connect((HOST, STAT_PORT))
    print("Report-Prozess verbunden.")

    while True:
        data = report_socket.recv(8)
        if not data:
            break
        mittelwert = struct.unpack('!d', data[:8])[0]
        summe = struct.unpack('!I', data[8:12])[0]

        #Ausgabe der Endergebnisse 
        print(f"Mittelwert: {mittelwert}, Summe: {summe}")
        #Pausierung des Prozesses für eine Sekunde
        time.sleep(1)
