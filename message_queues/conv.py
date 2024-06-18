import random
import time
#A/D-Converter
#prüft Messwerte auf Plausibilität (unklar) 
#konvertiert sie gegebenenfalls (unklar)
#Synchronisation(!)

def analog_to_digital_converter():
    #Eingangswert (zufällig zwischen 0-5 Volt)
    #double
    analog_value = random.uniform(0, 5)
    
    #analoger Wert in einen digitalen Wert (8Bit Auflösung)
    digital_value = int((analog_value /5)*255)
    #Binär oder dezimal? (unklar)

    return digital_value

def main():
    while True:
        
        # Ausgabe und Aufruf des Converters
        print("Digitaler Eingangswert:", analog_to_digital_converter())
        
        time.sleep(1)

if __name__ == "__main__":
    main()