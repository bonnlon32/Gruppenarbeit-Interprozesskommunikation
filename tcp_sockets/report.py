#enthält server der stat zuhört und mittelwert und summe bekommt
#gibt daten in shell aus


#Beispiel - noch nicht an die Aufgabe angepasst - nur Grundidee
import time

def report():
    #Summe und Mittelwert aus stat ausgeben
    
    wert= 3

    return wert

def main():
    while True:
        
        # Ausgabe der Endergebnisse 
        print("Ausgabewert:", report())
        
        #Pausierung des Prozesses für eine Sekunde
        time.sleep(1)

if __name__ == "__main__":
    main()
