import mmap # ermöglicht  direkten Zugriff auf Dateien im Speicher

#log_process
def write_log_datei(digital_value):  # Generierte Werte aus dem conv process müssen weiter gegeben werden
    with open("log.txt", "a") as f:  # Erstellen,bzw. öffnen der Datei log.txt im Modus append
        f.write(f"{digital_value}\n") # Schreiben in die Datei in eine neue Zeile

def log_process(shm_conv_log, semaphore_conv_log): 
    SHM_SIZE = 1024
    # Log-Prozess: Daten aus Shared Memory lesen und in eine Log-Datei schreiben
    while True:
        semaphore_conv_log.acquire()  # Warten auf Freigabe der Semaphore
        with mmap.mmap(shm_conv_log.fd, SHM_SIZE, access=mmap.ACCESS_READ) as mapfile: 
            mapfile.seek(0)
            data = mapfile.read(SHM_SIZE).decode().strip()  # Daten aus Shared Memory lesen
            write_log_datei(data)  # Daten in Log-Datei schreiben