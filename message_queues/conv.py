#A/D-Converter
import random
import time

def analog_to_digital_converter():         
    analog_value = random.uniform(0, 5) #Eingangswert (zufällig zwischen 0-5 Volt)
    #analoger Wert in einen digitalen Wert (8Bit Auflösung)
    digital_value = int((analog_value /5)*255)
    print(digital_value) # Ausgabe auf der Konsole
    time.sleep(0.4)  # Wartezeit, um die Werte in Intervallen zu generieren
    return digital_value