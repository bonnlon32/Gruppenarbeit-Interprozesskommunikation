import random
import os
import time

# Behilfscode (random Zahlen) für Test
def generate_random_number():
    random_number = random.uniform(-1, 5)
    return round(random_number, 2)

#Verzeichnis zum Speichern der Datei
#directory = "/path/to/your/directory"      #für Unix
directory = "C:\\Users\\noahr\\txtBSRN"     #für Windows


filename = os.path.join(directory, "random_numbers.txt")    # Datei, in die die zufälligen Zahlen geschrieben werden sollen

def main():

    while True:     # Endlosschleife
        
        number = generate_random_number()   #Funktionsaufruf Behilfscode
        
        with open(filename, "a") as file:   # Öffnet Datei im Anhangmodus (a = append)
            file.write(f"{number}\n")
        
        print(f"Zufallswert: {number}\t-> In die Datei '{filename}' geschrieben.") #Ausgabe
        
        time.sleep(1)


if __name__ == "__main__":
    main()