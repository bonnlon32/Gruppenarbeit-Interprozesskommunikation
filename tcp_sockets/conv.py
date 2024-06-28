#enthält client der random Zahlen zwischen 1-10 an stats und log schickt

import random #für random zahl
import time #für 1 sek abstände
import socket #für erstellung der sockets
import signal
import sys

HOST = "localhost" #localhost adresse (lokal auf dem betriebssystem ohne das netzwerk zu verlassen)
LOG_PORT = 5002
STAT_PORT = 5003  #beliebige zahl, nur manche adressen sind reserviert

log_socket = None
stat_socket = None
shutting_down = False

# Conv-Prozess: Generiert Zufallszahlen und sendet sie an Log und Stat
def conv_process():
    global log_socket, stat_socket
    try:
        #client erstellen und zu port verbinden
        log_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        stat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
        log_socket.connect((HOST, LOG_PORT))
        stat_socket.connect((HOST, STAT_PORT))

        while True:
         measuredValue = random.randint(-1, 10)  # Zufallszahl als Messwert
         if measuredValue < 0:      #unplausible Werte unter 0 umkonvertieren auf 0
            measuredValue= 0
            
         # Messwert als String und Zeilenumbruch senden
         data = str(measuredValue).encode('utf-8') #umschreiben
         log_socket.sendall(data + b'\n') #verschicken an log 
         stat_socket.sendall(data + b'\n') #verschicken an stats

         time.sleep(1)  # Wartezeit zwischen den Messungen
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if log_socket:
            log_socket.close()
        if stat_socket:
            stat_socket.close()

def signal_handler(sig, frame):
    global shutting_down
    if not shutting_down:
        shutting_down = True
        if log_socket:
            log_socket.close()
        if stat_socket:
            stat_socket.close()
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

#damit wir den conv_process auch in der main starten können
if __name__ == '__main__':
    conv_process()