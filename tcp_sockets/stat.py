#enthält server der zuhört und zahlen von conv bekommt

#rechnet mittelwert und summe aus werten zsm 
#mittelwert wird float- schwierig zu übertragen, also umgehen wir das und übertragen als integer und basteln am ende wieder als float zusammen

# enthält client der den mittelwert und summe an report schickt
    

#Beispiel - noch nicht an die Aufgabe angepasst - nur Grundidee

# Funktion zur Berechnung von Statistiken aus den Zufallszahlen
def statistikenBerechnen(zufallszahlen, pipe_name):
    summenwert = 0
    anzahl = 0
    zahlen = []

# Zufallszahlen aus der Datei lesen und Statistiken berechnen
    with open(zufallszahlen, 'r') as datei:
        for zeile in datei:
            zahl = int(zeile.strip())
            zahlen.append(zahl)
            summenwert += zahl
            anzahl += 1

# Mittelwert berechnen
    if anzahl > 0:
        durchschnitt = summenwert / anzahl
    else:
        durchschnitt = 0
   

