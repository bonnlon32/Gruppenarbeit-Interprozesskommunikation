#enthält server der zuhört und zahlen von conv bekommt
# enthält client der den mittelwert und summe an report schickt
    
import socket

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
    print(f"Verbindung von stat zu {addr} hergestellt.") # addr = Adresse des Clients, der die Verbindung hergestellt hat, addr ein Tupel (client_ip, client_port).

    #client
    report_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    report_socket.connect((HOST, STAT_PORT))
    print(f"Verbindung von report zu stat hergestellt.")
  
    total = 0
    average = 0
    count = 0

    buffer = b''
    while True:
            print("In while true Teil von stats gekommen")
            data = conn.recv(1024)  # Empfange bis zu 1024 Bytes 
            #fehler prävention
            # if not data:
            #          print("not data")
            #          break
            buffer += data
            while b'\n' in buffer:  # Verarbeite alle vollständigen Nachrichten im Puffer
             line, buffer = buffer.split(b'\n', 1)
             measuredValue = int(line.decode('utf-8'))  # Wandle die empfangenen Bytes in einen String und dann in einen Integer um
             total += measuredValue
             count += 1
             average = total / count
             data = f"{total},{average}"  # Summe und Durchschnitt als String mit Komma getrennt
             report_socket.sendall(data.encode('utf-8') + b'\n')  # Füge ein Newline-Zeichen hinzu
             print(f"Gesendet: {data}")

    conn.close()

if __name__ == '__main__':
    stat_process()
