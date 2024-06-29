#enthält server der stat zuhört und mittelwert und summe bekommt
#gibt daten in shell aus

import socket
import time
import sys
import signal

HOST = "localhost" 
REPORT_PORT = 5004

report_socket = None
shutting_down = False

# Report-Prozess: Gibt die statistischen Daten in der Shell aus
def report_process():
    global report_socket
    try:
        report_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #hey ich existiere
        report_socket.bind((HOST, REPORT_PORT))   #hey auf dem port bin ich
        report_socket.listen(1)    #hey ich höre jetzt auch anderen zu
        print(f"Report-Server listening on {HOST}:{REPORT_PORT}")
        conn, addr = report_socket.accept()   #hey ich seh dich jetzt
    


    
        buffer = b''     #buffer zum sammeln aller Daten, da bei tcp sockets oft daten in teilen empfangen werden
        while True:      #mindestens eine vollständige Nachricht im Buffer ist (endet mit \n)
            
            data = conn.recv(1024)  # Empfange bis zu 1024 Bytes 
            #fehler prävention
            if not data:
                    print("not data")
                    break
            buffer += data
            while b'\n' in buffer:  # Verarbeite alle vollständigen Nachrichten im Puffer
             line, buffer = buffer.split(b'\n', 1)  #extrahiert diese vollständige Nachricht bis zum ersten \n 
                                                    #und lässt den Rest der Daten im Buffer
                                                         
             total_str, average_str = line.decode('utf-8').split(',')  # Trenne Summe und Durchschnitt
             total = float(total_str)   #typecasting in float
             average = float(average_str)

             #Ausgabe der Endergebnisse 
             print(f"Empfangen - Summe: {total}, Durchschnitt: {average}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if report_socket:
            report_socket.close()

    #Pausierung des Prozesses für eine Sekunde
    time.sleep(1)
    
def signal_handler(sig, frame):
    global shutting_down
    if not shutting_down:
        shutting_down = True
        if report_socket:
            report_socket.close()
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

#damit wir den report_process auch in der main starten können
if __name__ == '__main__':
    report_process()