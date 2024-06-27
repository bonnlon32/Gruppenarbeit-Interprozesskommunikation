import mmap

def calculate_stats(zahlen_liste):
    calc_sum = sum(zahlen_liste)
    calc_quantity = len(zahlen_liste)
    calc_average = calc_sum / calc_quantity if calc_quantity > 0 else 0
    return calc_sum, calc_average

def stat_process(shm_conv_stat, semaphore_conv_stat, shm_stat_report, semaphore_stat_report):
    SHM_SIZE = 1024
    # Statistik-Prozess: Daten aus Shared Memory lesen, Statistiken berechnen und in Shared Memory schreiben
    zahlen_liste = []  # Liste für die Zahlen aus dem Shared Memory
    
    while True:
        semaphore_conv_stat.acquire()  # Warten auf Freigabe der Semaphore
        with mmap.mmap(shm_conv_stat.fd, SHM_SIZE, access=mmap.ACCESS_READ) as mapfile:
            mapfile.seek(0)
            data = mapfile.read(SHM_SIZE).decode().strip()  # Daten aus Shared Memory lesen
            
        try:
            new_numbers = list(map(int, data.split()))  # Daten in Zahlen umwandeln
        except ValueError as e:
            print(f"Fehler beim Konvertieren der Daten zu Zahlen: {e}")
            continue  # Bei Fehler die Schleife überspringen
        
        zahlen_liste.extend(new_numbers)  # Neue Zahlen zur Liste hinzufügen
        
        if zahlen_liste:  # Wenn Zahlen vorhanden sind, Statistiken berechnen
            summenwert, durchschnitt = calculate_stats(zahlen_liste)
        else:
            summenwert, durchschnitt = 0, 0  # Falls keine Zahlen vorhanden sind, Standardwerte verwenden
        
        # Statistiken in das Report-Prozess-Segment schreiben
        with mmap.mmap(shm_stat_report.fd, SHM_SIZE,access=mmap.ACCESS_WRITE) as mapfile:
            mapfile.seek(0)
            mapfile.write(f"{summenwert} {durchschnitt}".encode().ljust(SHM_SIZE))  # Daten schreiben und auffüllen
            mapfile.flush()
        semaphore_stat_report.release()  # Semaphore freigeben, um den Report-Prozess zu benachrichtigen
