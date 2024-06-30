import random
import time

#Dieser Endlosprozess simuliert einen A/D-Converter mit fiktionalen Messwerten und sendet sie an Log und stat_ mittels MessageQueue


def conv_process(mqToStat, mqToLog):
    time.sleep(1)


    while True:
        message = str(analog_to_digital_converter())                # Aufruf des Converters
        messageEncoded = message.encode()                           # Konvertierung Nachricht in Bytes)
        mqToLog.send(messageEncoded)                                # Sendet Nachricht zu Log
        mqToStat.send(messageEncoded)                               # Sendet Nachricht zu Stat 
        time.sleep(1)
    
         


def analog_to_digital_converter():
    #Gibt zufälligen Eingangswert (double zwischen -1 bis 5 Volt) aus, um A/D-Converter mit einschließlich nicht plausiblen Werten zu simulieren
    digital_value = round(random.uniform(-1, 10),2)   #gerundet auf 2 Nachkommastellen
    
    if digital_value < 0:        #Prüfung des Messwerts auf Plausibilität
        digital_value = 0        #Wenn Messwert nicht plausibel, wird auf 0 gesetzt
    
    return digital_value