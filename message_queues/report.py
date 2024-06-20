import random
import time

# Behilfscode (random Zahlen) für Test
def generate_random_number():
    random_number = random.uniform(-1, 5)
    return round(random_number, 2)

def main():

    while True:
        print(generate_random_number())     #Generierung & Ausgabe von Zahl
        time.sleep(1)


if __name__ == "__main__":
    main()