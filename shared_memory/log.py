#log_process
def write_log_datei(digital_value):  # Generierte Werte aus dem conv process müssen weiter gegeben werden
    with open("log.txt", "a") as f:  # Erstellen,bzw. öffnen der Datei log.txt im Modus append
        f.write(f"{digital_value}\n") # Schreiben in die Datei in eine neue Zeile