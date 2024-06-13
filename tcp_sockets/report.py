#enthält server der stat zuhört und mittelwert und summe bekommt
#gibt daten in shell aus
#kein client

import socket
import struct
import time

HOST = "localhost" 
REPORT_PORT = 5004

# Report-Prozess: Gibt die statistischen Daten in der Shell aus
def report_process():
    report_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #hey ich existiere
    report_socket.bind((HOST, REPORT_PORT))   #hey auf dem port bin ich
    report_socket.listen(1)    #hey ich höre jetzt auch anderen zu
    print(f"Server listening on {HOST}:{REPORT_PORT}")
    conn, addr = report_socket.accept()   #hey ich seh dich jetzt
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

if __name__ == '__main__':
    report_process()