import random
import time
#berechnet Mittelwert und Summe aus Conv

# Behilfscode (random Zahlen) für Test
def generate_random_number():
    random_number = random.uniform(-1, 5)
    return round(random_number, 2)



def main():

    avrg = 0.0
    sum = 0.0
    count = 0
    
    
    while True:

        count+=1
        num = generate_random_number()  #Ausgabe random Zahl
        sum += num                      #Berechnung Summe
        avrg = sum/count                #Berechnung Mittelwert

        #rundet und gibt aus
        print("Summe: ", round(sum,2))
        print("Mittelwert: ", round(avrg,2))

        time.sleep(0.2)
        



if __name__ == "__main__":
    main()