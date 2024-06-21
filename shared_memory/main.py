import os
import mmap
import posix_ipc
import time
from conv import analog_to_digital_converter
from log import write_log_datei
from stats import calculate_stats
from report import generate_report

# Definition der Namen für die Shared Memory Segmente
SHM_CONV_LOG_NAME = "/shared_memory_conv_log"
SHM_CONV_STAT_NAME = "/shared_memory_conv_stat"
SHM_STAT_REPORT_NAME = "/shared_memory_stat_report"

# Größe des Shared Memory Segments
SHM_SIZE = 1024  # Die Größe reicht in diesem Fall aus

def conv_process():
    # Erstellt und öffnet ein Shared Memory Segment für den jeweiligen Prozesses
    shm_conv_log = posix_ipc.SharedMemory(SHM_CONV_LOG_NAME, posix_ipc.O_CREAT, size=SHM_SIZE)
    shm_conv_stat = posix_ipc.SharedMemory(SHM_CONV_STAT_NAME, posix_ipc.O_CREAT, size=SHM_SIZE)
    shm_stat_report = posix_ipc.SharedMemory(SHM_STAT_REPORT_NAME, posix_ipc.O_CREAT, size=SHM_SIZE)
# shm_stat_report = posix_ipc.SharedMemory(SHM_STAT_REPORT_NAME, posix_ipc.O_CREAT, size=SHM_SIZE)
    # Erstellt und öffnet ein Semaphor für die Synchronisation des jeweiligen Speichers
    semaphore_conv_log = posix_ipc.Semaphore("/semaphore_conv_log", posix_ipc.O_CREAT, initial_value=0)
    semaphore_conv_stat = posix_ipc.Semaphore("/semaphore_conv_stat", posix_ipc.O_CREAT, initial_value=0)
    semaphore_stat_report = posix_ipc.Semaphore("/semaphore_stat_report", posix_ipc.O_CREAT, initial_value=0)
# semaphore_stat_report = posix_ipc.Semaphore("/semaphore_stat_report", posix_ipc.O_CREAT, initial_value=0)
    
    # Starten des Log-Prozesses durch Forken des aktuellen Prozesses
    pid_log = os.fork()
    if pid_log == 0:
        log_process(shm_conv_log, semaphore_conv_log)
        os._exit(0)
    
    # Starten des Stat-Prozesses durch Forken des aktuellen Prozesses
    pid_stat = os.fork()
    if pid_stat == 0:
        stat_process(shm_conv_stat, semaphore_conv_stat)
        os._exit(0)

    while True:      
        # Generieren eines neuen Wertes und direktes Umwandeln in Bytes
        data = str(analog_to_digital_converter()).encode()
        
        # Schreiben der Daten in den Shared Memory des Log-Speichers
        with mmap.mmap(shm_conv_log.fd, SHM_SIZE) as mapfile:
            mapfile.seek(0)
            mapfile.write(data.ljust(SHM_SIZE))  # Auffüllen mit Leerzeichen, um alte Daten zu überschreiben
            mapfile.flush()
        semaphore_conv_log.release()  # Freigeben des Semaphors, um den Log-Prozess zu benachrichtigen
        
        # Kurze Pause, um den Datenfluss zu verlangsamen und die Ausgabe zu synchronisieren
        time.sleep(1)

def log_process(shm_conv_log, semaphore_conv_log):
    while True:
        semaphore_conv_log.acquire()  # Warten, bis neue Daten verfügbar sind
        with mmap.mmap(shm_conv_log.fd, SHM_SIZE) as mapfile:
            mapfile.seek(0)
            data = mapfile.read(SHM_SIZE).decode().strip()  # Lesen und Dekodieren der Daten
            write_log_datei(data)  # Schreiben der Daten in die Log-Datei

def stat_process(shm_conv_stat, semaphore_conv_stat):
    zahlen_liste = []
    
    while True:
        semaphore_conv_stat.acquire()  # Warten, bis neue Daten verfügbar sind
        with mmap.mmap(shm_conv_stat.fd, SHM_SIZE) as mapfile:
            mapfile.seek(0)
            data = mapfile.read(SHM_SIZE).decode().strip()  # Lesen und Dekodieren der Daten
        
        # Umwandeln der eingelesenen Daten in eine Liste von Zahlen
        new_numbers = list(map(int, data.split()))
        zahlen_liste.extend(new_numbers)
        
        # Berechnen von Summenwert und Durchschnitt aus der Zahlenliste
        summenwert, durchschnitt = calculate_stats(zahlen_liste)
        semaphore_conv_stat.release()  # Freigeben des Semaphors
def report_process(shm_stat_report, semaphore_stat_report):
    # Report-Prozess: Statistiken aus Shared Memory lesen und Bericht generieren
    while True:
        semaphore_stat_report.acquire()  # Warten auf Freigabe der Semaphore
        with mmap.mmap(shm_stat_report.fd, SHM_SIZE,access=mmap.ACCESS_READ) as mapfile:
            mapfile.seek(0)
            data = mapfile.read(SHM_SIZE).decode().strip()  # Daten aus Shared Memory lesen
        
        # Statistiken aus den Daten extrahieren und Bericht generieren
        summenwert, durchschnitt = map(float, data.split())
        generate_report(summenwert, durchschnitt)  # Bericht generieren



# Starten des Conv-Prozesses
if __name__ == "__main__":
    conv_process()
