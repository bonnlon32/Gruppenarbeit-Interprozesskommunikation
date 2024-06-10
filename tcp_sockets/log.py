#enthält server der zuhört und von client aus conv daten bekommt
#schreibt daten in eine datei und speichert ab

#Beispiel - noch nicht an die Aufgabe angepasst - nur Grundidee
def write_log_file(messw):
    with open("log.txt", "a") as log:
        log.write("Der Messwert ist: " + str(messw) + "\n")

if __name__ == "__main__":
    main()