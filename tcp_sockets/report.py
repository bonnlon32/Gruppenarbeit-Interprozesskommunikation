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
    print(f"Verbindung von Report zu {addr} hergestellt.")


    while True:
        data = conn.recv(12)
        if not data:
            break
        average = struct.unpack('!f', data[:8])[0]
        total = struct.unpack('!d', data[8:12])[0]

        #!f steht für einen 4-Byte-Float im Network Byte Order
        #!d steht für einen 8-Byte-Double im Network Byte Order
        #!I steht für einen 4-Byte-Unsigned-Integer im Network Byte Order

        #Ausgabe der Endergebnisse 
        print(f"Mittelwert: {average}, Summe: {total}")
        #Pausierung des Prozesses für eine Sekunde
        time.sleep(1)

if __name__ == '__main__':
    report_process()