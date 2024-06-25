import mmap 
def generate_report(summenwert, durchschnitt):
    print(f"Report: Summe = {summenwert}, Mittelwert = {durchschnitt}")

def report_process(shm_stat_report, semaphore_stat_report):
    # Report-Prozess: Statistiken aus Shared Memory lesen und Bericht generieren
    SHM_SIZE = 1024

    while True:
        semaphore_stat_report.acquire()  # Warten auf Freigabe der Semaphore
        with mmap.mmap(shm_stat_report.fd, SHM_SIZE,access=mmap.ACCESS_READ) as mapfile:
            mapfile.seek(0)
            data = mapfile.read(SHM_SIZE).decode().strip()  # Daten aus Shared Memory lesen
        
        # Statistiken aus den Daten extrahieren und Bericht generieren
        summenwert, durchschnitt = map(float, data.split())
        generate_report(summenwert, durchschnitt)  # Bericht generieren