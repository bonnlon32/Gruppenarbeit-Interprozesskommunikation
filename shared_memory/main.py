import os           # Modul für Betriebssystem-Funktionen
import posix_ipc    # Modul für Funktionen der Interprozesskommunikation gemäß Standards
import signal       # Modul für das Behandeln von Signalen wie SIGINT (Ctrl+C)
import sys          # Modul zur Systemmanipulation (z.B. zum Beenden des Programms)

# Importieren der einzelnen Prozesse:
from conv import conv_process
from stats import stat_process
from report import report_process
from log import log_process

def signal_handler(sig, frame):
    print("Abbruchsignal empfangen. Prozesse werden beendet...") # Wird ausgegeben
    cleanup(sig, frame)      # Aufruf der Cleanup-Funktion
    sys.exit(0)  # Beendet das Programm

def cleanup(signum, frame):
    print("Cleaning up shared memory and semaphores...")
    try:
        posix_ipc.unlink_shared_memory(SHM_CONV_LOG_NAME)
        posix_ipc.unlink_shared_memory(SHM_CONV_STAT_NAME)
        posix_ipc.unlink_shared_memory(SHM_STAT_REPORT_NAME)
        posix_ipc.unlink_semaphore("/semaphore_conv_log")
        posix_ipc.unlink_semaphore("/semaphore_conv_stat")
        posix_ipc.unlink_semaphore("/semaphore_stat_report")
    except Exception as e:
        print(f"Error during cleanup: {e}")
    sys.exit(0)

if __name__ == "__main__":

    # Größe für alle Shared Memory Segmente (in Bytes)
    SHM_SIZE = 1024
    
    # Namen für die Shared Memory Segmente
    SHM_CONV_LOG_NAME = "/shared_memory_conv_log"
    SHM_CONV_STAT_NAME = "/shared_memory_conv_stat"
    SHM_STAT_REPORT_NAME = "/shared_memory_stat_report"

    # Shared Memory für die jeweiligen Segmente erstellen
    shm_conv_log = posix_ipc.SharedMemory(SHM_CONV_LOG_NAME, posix_ipc.O_CREAT, size=SHM_SIZE)
    shm_conv_stat = posix_ipc.SharedMemory(SHM_CONV_STAT_NAME, posix_ipc.O_CREAT, size=SHM_SIZE)
    shm_stat_report = posix_ipc.SharedMemory(SHM_STAT_REPORT_NAME, posix_ipc.O_CREAT, size=SHM_SIZE)
    
    # Semaphore für die jeweiligen Segmente erstellen 
    semaphore_conv_log = posix_ipc.Semaphore("/semaphore_conv_log", posix_ipc.O_CREAT, initial_value=0)
    semaphore_conv_stat = posix_ipc.Semaphore("/semaphore_conv_stat", posix_ipc.O_CREAT, initial_value=0)
    semaphore_stat_report = posix_ipc.Semaphore("/semaphore_stat_report", posix_ipc.O_CREAT, initial_value=0)
    
    try:
        # Erstellen des Prozessgerüstes mithilfe von fork()
        pid_conv = os.fork() 
        if pid_conv == 0:
            conv_process(shm_conv_log,shm_conv_stat,semaphore_conv_log, semaphore_conv_stat)  # Hauptfunktionsaufruf für den conv-process
            os._exit(0)


        pid_log = os.fork()
        if pid_log == 0:
            log_process(shm_conv_log, semaphore_conv_log)
            os._exit(0)
        
        pid_stat = os.fork()
        if pid_stat == 0:
            stat_process(shm_conv_stat, semaphore_conv_stat, shm_stat_report, semaphore_stat_report)
            os._exit(0)
        
        pid_report = os.fork()
        if pid_report == 0:
            report_process(shm_stat_report, semaphore_stat_report)
            os._exit(0)
        signal.signal(signal.SIGINT, signal_handler) # Registriere einen Signalhandler für SIGINT (Ctrl+C), um das Programm zu beenden 
        os.wait()
        
        
    except KeyboardInterrupt as e:
        sys.exit(0)   # Beende das Programm mit einem Erfolgscode (0 steht für erfolgreichen Abschluss) 
