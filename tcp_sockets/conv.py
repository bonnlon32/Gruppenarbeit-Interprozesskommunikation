#enthält client der random Zahlen zwischen 1-10 an stats und log schickt

import random #für random zahl
import time #für 1 sek abstände
import socket #für erstellung der sockets
import signal    #Importiert das Modul für Signalverarbeitung
import sys      #Importiert das Modul zur Interaktion mit dem Interpreter

HOST = "localhost" #localhost adresse (lokal auf dem betriebssystem ohne das netzwerk zu verlassen)
LOG_PORT = 5002
STAT_PORT = 5003  #beliebige zahl, nur manche adressen sind reserviert

#Initialisierung der Sockets und der Variable shutting_down 
log_socket = None           #zum sicherstellen, dass sie im globalen Namensraum existieren
stat_socket = None
shutting_down = False        #programm ist nicht im prozess des runterfahrens

#Conv-Prozess: Generiert Zufallszahlen und sendet sie an Log und Stat
def conv_process():
    global log_socket, stat_socket      #global um zugriff auch innerhalb der anderen Dateien zu gewährleisten
    try:
         #Erstellen und Verbinden des Log-Sockets
        log_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        log_socket.connect((HOST, LOG_PORT))
         #Erstellen und Verbinden des Stat-Sockets
        stat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        stat_socket.connect((HOST, STAT_PORT))

        while True:
         measuredValue = random.randint(-1, 10)  #Zufallszahl als Messwert
         if measuredValue < 0:      #unplausible Werte unter 0 umkonvertieren auf 0
            measuredValue= 0
            
        #Konvertiert den Wert in Bytes und fügt einen Zeilenumbruch hinzu
         data = str(measuredValue).encode('utf-8') 
         log_socket.sendall(data + b'\n') #verschicken an log 
         stat_socket.sendall(data + b'\n') #verschicken an stats

         time.sleep(1)  #Wartezeit 1 Sekunde zwischen den Messungen
    #Fehler abfangen     
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if log_socket:
            log_socket.close()   #Schließen des Log-Sockets, falls geöffnet
        if stat_socket:
            stat_socket.close()    #Schließen des Stat-Sockets, falls geöffnet

#Signal handler zum beenden des Programms und schließen der Sockets
def signal_handler(sig, frame):  
    global shutting_down           #global, damit der signal handler sie global deklarieren kann, obwohl sie außerhalb definiert ist
    if not shutting_down:           #stellt sicher das folgender code nur ausgefürt ist, falls nicht vorher schon shutting_down läuft
        shutting_down = True       #hier wird nun das programm auf runterfahren gestellt
        #schließt socket falls er existiert
        if log_socket:              
            log_socket.close()      
        if stat_socket:
            stat_socket.close()       
        sys.exit(0)         #beendet das Programm und gibt alle offenen Ressourcen frei

#Registrieren des signal handlers
signal.signal(signal.SIGINT, signal_handler)        #interrupt signal wird gesendet wenn strg+c gedrückt wird
signal.signal(signal.SIGTERM, signal_handler)          #terminate signal wird verwendet um programm zu beenden

#damit wir den conv_process auch in der main starten können
if __name__ == '__main__':
    conv_process()