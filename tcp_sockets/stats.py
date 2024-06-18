#enthält server der zuhört und zahlen von conv bekommt
# enthält client der den mittelwert und summe an report schickt
    
import socket
import struct

HOST = "localhost" 
STAT_PORT = 5003
REPORT_PORT = 5004

# Stat-Prozess: Berechnet Mittelwert und Summe der Messwerte
def stat_process():
    #server existieren lassen, da sein lassen, zuhören lassen und andere sehen lassen
    stat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    stat_socket.bind((HOST, STAT_PORT))
    stat_socket.listen(1)
    print("Stat-Prozess gestartet und wartet auf Verbindungen...")
    conn, addr = stat_socket.accept()
    print(f"Verbindung zu {addr} hergestellt.") # addr = Adresse des Clients, der die Verbindung hergestellt hat, addr ein Tupel (client_ip, client_port).

    #client
    report_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    report_socket.connect((HOST, STAT_PORT))
    print(f"Verbindung zu stat hergestellt.")
  
    total = 0
    average = 0
    count = 0

    while True:
        data = conn.recv(4) #nicht nur 4 byte weil float empfangen wird??? oder doch möglich?
        if not data:
            break
        messwert = struct.unpack('!I', data)[0]
        total += messwert
        count += 1
        average = total / count
        report_socket.sendall(struct.pack('!f', average))
        report_socket.sendall(struct.pack('!d', total))

if __name__ == '__main__':
    stat_process()
