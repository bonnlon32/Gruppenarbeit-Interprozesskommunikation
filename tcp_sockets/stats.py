# enthält server der zuhört und zahlen von conv bekommt
# enthält client der den mittelwert und summe an report schickt
    
import socket  #zur Erstellung von Sockets
import sys
import signal

HOST = "localhost" 
STAT_PORT = 5003
REPORT_PORT = 5004

stat_socket = None
report_socket = None
shutting_down = False


# Stat-Prozess: Berechnet Mittelwert und Summe der Messwerte
def stat_process():
    global stat_socket, report_socket
    try:
        #server existieren lassen, da sein lassen, zuhören lassen und andere sehen lassen
        stat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        stat_socket.bind((HOST, STAT_PORT))
        stat_socket.listen(1)
        print(f"Stat-Server listening on {HOST}:{STAT_PORT}")
        conn, addr = stat_socket.accept()
         # addr = Adresse des Clients, der die Verbindung hergestellt hat, addr ein Tupel (client_ip, client_port).

        #client
        report_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        report_socket.connect((HOST, REPORT_PORT))

        #konstanten zuweisung
        total = 0
        average = 0
        count = 0

        buffer = b'' #Erstellen buffer und fügen unsere Daten dort hinzu 
        while True:
           
            data = conn.recv(1024)  # Empfange bis zu 1024 Bytes 
            buffer += data
            while b'\n' in buffer:  # Verarbeite alle vollständigen Nachrichten im Puffer
             line, buffer = buffer.split(b'\n', 1)      #extrahiert diese vollständige Nachricht bis zum ersten \n 
                                                        #und lässt den Rest der Daten im Buffer

             measuredValue = int(line.decode('utf-8'))  # Wandle die empfangenen Bytes in einen String und dann in einen Integer um
            #fehler prävention
             if not measuredValue:
                     print("not measuredValue")
                     break
             #Ausgabe des random Messwertes
             print("Der Messwert ist ", measuredValue)
             #Berechnung Summe und Mittelwert
             total += round(measuredValue,2)    #Rundung auf zwei Nachkommastellen
             count += 1
             average = round(total / count,2)
             data = f"{total},{average}"  # Summe und Durchschnitt als String mit Komma getrennt
             report_socket.sendall(data.encode('utf-8') + b'\n')  # Füge ein Newline-Zeichen hinzu
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if stat_socket:
            stat_socket.close()
        if report_socket:
            report_socket.close()

def signal_handler(sig, frame):
    global shutting_down
    if not shutting_down:
        shutting_down = True
        #print('Control-C received and program is closing...')
        if stat_socket:
            stat_socket.close()
        if report_socket:
            report_socket.close()
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

#damit wir den stats_process auch in der main starten können
if __name__ == '__main__':
    stat_process()
