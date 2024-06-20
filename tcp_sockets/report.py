#enthält server der stat zuhört und mittelwert und summe bekommt
#gibt daten in shell aus
#kein client

import socket
import time

HOST = "localhost" 
REPORT_PORT = 5004

# Report-Prozess: Gibt die statistischen Daten in der Shell aus
def report_process():
    report_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #hey ich existiere
    report_socket.bind((HOST, REPORT_PORT))   #hey auf dem port bin ich
    report_socket.listen(1)    #hey ich höre jetzt auch anderen zu
    print(f"Report-Server listening on {HOST}:{REPORT_PORT}")
    conn, addr = report_socket.accept()   #hey ich seh dich jetzt
    


    
    buffer = b''
    while True:
            
            data = conn.recv(1024)  # Empfange bis zu 1024 Bytes 
            #fehler prävention
            if not data:
                    print("not data")
                    break
            buffer += data
    
            while b'\n' in buffer:  # Verarbeite alle vollständigen Nachrichten im Puffer
             line, buffer = buffer.split(b'\n', 1)
             total_str, average_str = line.decode('utf-8').split(',')  # Trenne Summe und Durchschnitt
             total = float(total_str)
             average = float(average_str)

             #Ausgabe der Endergebnisse 
             print(f"Empfangen - Summe: {total}, Durchschnitt: {average}")

        #!f steht für einen 4-Byte-Float im Network Byte Order
        #!d steht für einen 8-Byte-Double im Network Byte Order
        #!I steht für einen 4-Byte-Unsigned-Integer im Network Byte Order

        

    #Pausierung des Prozesses für eine Sekunde
    time.sleep(1)

if __name__ == '__main__':
    report_process()