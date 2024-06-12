import random
import time

def analog_to_digital_converter():
    #Eingangswert (zufällig zwischen 0-5 Volt)
    #double
    analog_value = random.uniform(0, 5)
    #analoger Wert in einen digitalen Wert (8Bit Auflösung)
    digital_value = int((analog_value /5)*255)
    #Binär oder dezimal? (unklar)
    print(digital_value)
    return digital_value
