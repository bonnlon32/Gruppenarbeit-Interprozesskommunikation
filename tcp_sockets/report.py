#enthält server der stat zuhört und mittelwert und summe bekommt
#gibt daten in shell aus

import socket    #für erstellung der sockets
import time     #für 1 sek abstände
import signal    #Importiert das Modul für Signalverarbeitung
import sys      #Importiert das Modul zur Interaktion mit dem Interpreter

HOST = "localhost" 
REPORT_PORT = 5004

#Initialisierung der Sockets und der Variable shutting_down
report_socket = None         #zum sicherstellen, dass er im globalen Namensraum existiert
shutting_down = False        #programm ist nicht im prozess des runterfahrens

#Report-Prozess: Gibt die statistischen Daten in der Shell aus
def report_process():
    global report_socket             #global um zugriff auch innerhalb der anderen Dateien zu gewährleisten
    try:
        report_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #hey ich existiere
        report_socket.bind((HOST, REPORT_PORT))   #hey auf dem port bin ich
        report_socket.listen(1)    #hey ich höre jetzt auch anderen zu
        print(f"Report-Server listening on {HOST}:{REPORT_PORT}")
        conn, addr = report_socket.accept()   #hey ich seh dich jetzt
    


    
        buffer = b''     #buffer zum sammeln aller Daten, da bei tcp sockets oft daten in teilen empfangen werden
        while True:      #mindestens eine vollständige Nachricht im Buffer ist (endet mit \n)
            
            data = conn.recv(1024)  #Empfange bis zu 1024 Bytes 
            #fehler prävention
            if not data:
                    print("not data")    #falls falsche oder unvollständige daten empfangen werden
                    break           #Verbindung schließen
            buffer += data
            while b'\n' in buffer:  #Verarbeitet alle vollständigen Nachrichten im Puffer
             line, buffer = buffer.split(b'\n', 1)  #extrahiert diese vollständige Nachricht bis zum ersten \n 
                                                    #und lässt den Rest der Daten im Buffer
                                                         
             total_str, average_str = line.decode('utf-8').split(',')  #Trennt Summe und Durchschnitt
             total = float(total_str)   #typecasting in float
             average = float(average_str)

             #Ausgabe der Endergebnisse 
             print(f"Empfangen - Summe: {total}, Durchschnitt: {average}")

    #Fehler abfangen 
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if report_socket:
            report_socket.close()        #Schließen des Sockets, falls geöffnet

    #Pausierung des Prozesses für eine Sekunde
    time.sleep(1)
    
#Signal handler zum beenden des Programms und schließen der Sockets    
def signal_handler(sig, frame):
    global shutting_down        #global, damit der signal handler sie global deklarieren kann, obwohl sie außerhalb definiert ist
    if not shutting_down:               #stellt sicher das folgender code nur ausgefürt ist, falls nicht vorher schon shutting_down läuft
        shutting_down = True         #hier wird nun das programm auf runterfahren gestellt
         #schließt socket falls er existiert
        if report_socket:
            report_socket.close()
        sys.exit(0)         #beendet das Programm und gibt alle offenen Ressourcen frei

#Registrieren des signal handlers
signal.signal(signal.SIGINT, signal_handler)        #interrupt signal wird gesendet wenn strg+c gedrückt wird
signal.signal(signal.SIGTERM, signal_handler)          #terminate signal wird verwendet um programm zu beenden

#damit wir den report_process auch in der main starten können
if __name__ == '__main__':
    report_process()