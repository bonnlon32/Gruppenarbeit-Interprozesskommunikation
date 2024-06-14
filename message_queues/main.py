import os
import mmap
import posix_ipc
from conv import analog_to_digital_converter
from log import write_log_datei


# Konstanten für den Shared Memory-Namen und die Größe
SHM_NAME_1 = "/shared_memory_1"
SHM_SIZE = 1024

def conv_process():
    # Shared Memory für Log erstellen
    shm_log = posix_ipc.SharedMemory(SHM_NAME_1, posix_ipc.O_CREAT, size=SHM_SIZE)
    semaphore = posix_ipc.Semaphore("/semaphore_1", posix_ipc.O_CREAT, initial_value=0)

    # Log-Prozess erstellen
    pid_log = os.fork()
    if pid_log == 0:
        log_process()
        os._exit(0)
        
def log_process():
    # Funktionalität des Log-Prozesses
    semaphore = posix_ipc.Semaphore("/semaphore_1")
    shm_log = posix_ipc.SharedMemory(SHM_NAME_1)
    
    while True:
        semaphore.acquire()  # Warten, bis neue Daten verfügbar sind
        
        with mmap.mmap(shm_log.fd, SHM_SIZE) as mapfile:
            mapfile.seek(0)
            data = mapfile.read(SHM_SIZE).decode().strip()  # Nur relevante Daten lesen und dekodieren
        
        write_log_datei(data)  # Schreiben der Daten in die Log-Datei
        
# Starten des Conv-Prozesses
conv_process()