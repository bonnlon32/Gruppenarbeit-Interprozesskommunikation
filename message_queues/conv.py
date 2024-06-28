import random
import time
import sys
import posix_ipc


#A/D-Converter


def conv_process(mqToStat, mqToLog):

    print("- - - CONV-PROZESS\t GESTARTET - - -")

    try:
        while True:
            message = str(analog_to_digital_converter())        #Aufruf des Converters
            #print("CONV Digitaler Eingangswert:", message)
            message = message.encode()                          #Konvertierung Nachricht in Bytes)
            mqToLog.send(message)                               #Sendet Nachricht zu Log
            mqToStat.send(message)                              #Sendet Nachricht zu Stat


#Timeoutcode
#            try:
#
#            except posix_ipc.BusyError:
#                print("CONV Timeout bei mQueue Conv to log")
#                mqToLog.close()
#                raise

            time.sleep(1)

    except KeyboardInterrupt:
         pass

         


def analog_to_digital_converter():
    #Gibt zufälligen Eingangswert (double zwischen -1 bis 5 Volt) aus, um A/D-Converter mit einschließlich nicht plausiblen Werten zu simulieren
    digital_value = round(random.uniform(-1, 10),2)   #gerundet auf 2 Nachkommastellen
    
    if digital_value < 0:        #Prüfung des Messwerts auf Plausibilität
        digital_value = 0        #Wenn Messwert nicht plausibel, wird auf 0 gesetzt
    
    return digital_value