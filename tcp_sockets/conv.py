#random zahl wird erstellt
#client schickt diese zahl an log und stat

#Beispiel - noch nicht an die Aufgabe angepasst - nur Grundidee
import random
#mit server anfangen und nicht client!

# Funktion zum Schreiben von Zufallszahlen in eine Datei
def schreibe_zufallszahlen_in_datei(zufallszahlen, anzahl=5):
    with open(zufallszahlen, 'w') as datei:
        for _ in range(anzahl):
            zahl = random.randint(0, 100)
            datei.write(f"{zahl}\n")

# Zufallszahlen in Datei schreiben
    schreibe_zufallszahlen_in_datei(zufallszahlen)

