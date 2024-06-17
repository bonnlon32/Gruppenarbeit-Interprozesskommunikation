import os
import mmap
import posix_ipc
from conv import analog_to_digital_converter
from log import write_log_datei


# Konstanten für den Shared Memory-Namen und die Größe
SHM_NAME_1 = "/shared_memory_1"
SHM_SIZE = 4096 # Änderung auf größere Speicherkapazität, damit es weiterhin funktioniert

def conv_process():
    shm_log = posix_ipc.SharedMemory(SHM_NAME_1, posix_ipc.O_CREAT, size=SHM_SIZE)
    semaphore = posix_ipc.Semaphore("/semaphore_1", posix_ipc.O_CREAT, initial_value=0)
    
    pid_log = os.fork()
    if pid_log == 0:
        log_process()
        os._exit(0)

    while True:      
        data = str(analog_to_digital_converter()).encode()  # Generieren des neuen Wertes und direktes Umwandeln der Daten in Bytes
        
        with mmap.mmap(shm_log.fd, SHM_SIZE) as mapfile:
            mapfile.seek(0)
            mapfile.write(data.ljust(SHM_SIZE))  # Padding mit Leerzeichen, um alte Daten zu überschreiben
            mapfile.flush()
        semaphore.release()  # Signal an log_process und stat_process, dass neue Daten verfügbar sind

def log_process():
    semaphore = posix_ipc.Semaphore("/semaphore_1")
    shm_log = posix_ipc.SharedMemory(SHM_NAME_1)
    
    while True:
        semaphore.acquire()
        with mmap.mmap(shm_log.fd, SHM_SIZE) as mapfile:
            mapfile.seek(0)
            data = mapfile.read(SHM_SIZE).decode().strip()
        
# Starten des Conv-Prozesses        
if __name__ == "__main__":
    conv_process()
