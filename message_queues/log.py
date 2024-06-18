import random
import os
import time

# Behilfscode (random Zahlen) für Test
def generate_random_number():
    random_number = random.uniform(-1, 5)
    return round(random_number, 2)

#Verzeichnis zum Speichern der Datei
#directory = "/path/to/your/directory"      #Unix
directory = "C:\\Users\\noahr\\txtBSRN"     #Windows


filename = os.path.join(directory, "random_numbers.txt")    # Datei, in die die zufälligen Zahlen geschrieben werden sollen



while True:     # Endlosschleife
    
    number = generate_random_number()   #Funktionsaufruf Behilfscode
    
    with open(filename, "a") as file:   # Öffnet Datei im Anhangmodus (a = append)
        file.write(f"{number}\n")
    
    print(f"Random: {number} in die Datei '{filename}' geschrieben.")
    
    time.sleep(1)
