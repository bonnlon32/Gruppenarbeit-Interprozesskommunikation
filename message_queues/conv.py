import random
import time
import sys
#import posix_ipc

#A/D-Converter
#Synchronisation(!)
#Binär oder Dezimal -> ist unsere Wahl

def analog_to_digital_converter():
    #Gibt zufälligen Eingangswert (double zwischen -1 bis 5 Volt) aus, um A/D-Converter mit einschließlich nicht plausiblen Werten zu simulieren
    digital_value = round(random.uniform(-1, 10),2)   #gerundet auf 2 Nachkommastellen
    
    if digital_value < 0:        #Prüfung des Messwerts auf Plausibilität
        digital_value = 0        #Wenn Messwert nicht plausibel, wird auf 0 gesetzt
    
    return digital_value
    

def main():
    while True:
        
        print("Digitaler Eingangswert:", analog_to_digital_converter())  # Ausgabe und Aufruf des Converters
        
        time.sleep(1)

if __name__ == "__main__":
    main()