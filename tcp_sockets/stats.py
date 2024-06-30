# enthält server der zuhört und zahlen von conv bekommt
# enthält client der den mittelwert und summe an report schickt
    
import socket  #zur Erstellung von Sockets
import signal    #Importiert das Modul für Signalverarbeitung
import sys      #Importiert das Modul zur Interaktion mit dem Interpreter

HOST = "localhost" 
STAT_PORT = 5003
REPORT_PORT = 5004

#Initialisierung der Sockets und der Variable shutting_down
stat_socket = None      #zum sicherstellen, dass sie im globalen Namensraum existieren
report_socket = None
shutting_down = False        #programm ist nicht im prozess des runterfahrens


# Stat-Prozess: Berechnet Mittelwert und Summe der Messwerte
def stat_process():
    global stat_socket, report_socket        #global um zugriff auch innerhalb der anderen Dateien zu gewährleisten
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

        #konstanten initialisierung
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
            #Fehler abfangen 
             if measuredValue is None:     #püft ob daten empfangen worden sind
                     print("Kein measured Value empfangen.")     
                     break                  #Verbindung schließen
             #Ausgabe des random Messwertes
             print("Der Messwert ist ", measuredValue)
             #Berechnung Summe und Mittelwert
             total += round(measuredValue,2)    #Rundung auf zwei Nachkommastellen
             count += 1
             average = round(total / count,2)
             data = f"{total},{average}"  # Summe und Durchschnitt als String mit Komma getrennt
             report_socket.sendall(data.encode('utf-8') + b'\n')  # Füge ein Newline-Zeichen hinzu

    #Fehler abfangen 
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if stat_socket:
            stat_socket.close()          #Schließen des Sockets, falls geöffnet
        if report_socket:
            report_socket.close()        #Schließen des Sockets, falls geöffnet

#Signal handler zum beenden des Programms und schließen der Sockets
def signal_handler(sig, frame):
    global shutting_down        #global, damit der signal handler sie global deklarieren kann, obwohl sie außerhalb definiert ist
    if not shutting_down:           #stellt sicher das folgender code nur ausgefürt ist, falls nicht vorher schon shutting_down läuft
        shutting_down = True         #hier wird nun das programm auf runterfahren gestellt
         #schließt socket falls er existiert
        if stat_socket:
            stat_socket.close()
        if report_socket:
            report_socket.close()
        sys.exit(0)         #beendet das Programm und gibt alle offenen Ressourcen frei

#Registrieren des signal handlers
signal.signal(signal.SIGINT, signal_handler)        #interrupt signal wird gesendet wenn strg+c gedrückt wird
signal.signal(signal.SIGTERM, signal_handler)          #terminate signal wird verwendet um programm zu beenden

#damit wir den stats_process auch in der main starten können
if __name__ == '__main__':
    stat_process()
