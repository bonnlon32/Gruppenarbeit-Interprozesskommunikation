import random
import os
import time

def log_process():

    filename = "random_numbers.txt"    # Dateiname, in die die zufälligen Zahlen geschrieben werden sollen

    while True:     # Endlosschleife
        
        digital_num = generate_random_number()   #Funktionsaufruf Behilfscode
        
        with open(filename, "a") as file:   # Öffnet Datei im Anhangmodus (a = append)
            file.write(f"{digital_num}\n")
        
        print(f"Zufallswert: {digital_num}\t-> In die Datei '{filename}' geschrieben.") #Ausgabe
        
        time.sleep(1)


# Behilfscode (random Zahlen) für Test
def generate_random_number():
    random_number = random.uniform(-1, 10)
    return round(random_number, 2)