import os
import random
# Erster Entwurf für den Conv-Prozess. Hier werden Zufallszahlen generiert die später weiterverarbeitet werden

                                                   # Funktion simuliert einen A/D-Wandler(Von Noah).
def analog_to_digital_converter():
    analog_value = random.uniform(0, 5)            # Erzeugt einen zufälligen analogen Wert zwischen 0 und 5 Volt.
    digital_value = int((analog_value / 5) * 255)  # Konvertiert den analogen Wert in einen digitalen Wert (8-Bit-Auflösung).
    return digital_value


def conv_process():
     pipe_log = '/tmp/conv_to_log'    # Pfad zur benannten Pipe für den Log-Prozess
     pipe_stat = '/tmp/conv_to_stat'  # Pfad zur benannten Pipe für den Stat-Prozess
     pass

if __name__ == "__main__":
    # Startet den Conv-Prozess
    conv_process()