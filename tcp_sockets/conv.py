#enthält client der random Zahlen zwischen 1-10 an stats und log schickt

import random #für random zahl
import time #für 1 sek abstände
import socket #für erstellung der sockets

# Konstanten für Host und Ports (wohin?? hier rein oder main?)
HOST = "localhost" #localhost adresse (lokal auf dem betriebssystem ohne das netzwerk zu verlassen)
LOG_PORT = 5002
STAT_PORT = 5003  #beliebige zahl, nur manche adressen sind reserviert



# Conv-Prozess: Generiert Zufallszahlen und sendet sie an Log und Stat
def conv_process():

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

#damit wir den conv_process auch in der main starten können
if __name__ == '__main__':
    conv_process()