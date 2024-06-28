import random # Modul zur Generierung von Zahlen 
import time
import mmap 

SHM_CONV_LOG_NAME = "/shared_memory_conv_log"

def analog_to_digital_converter():         
     #Gibt zufälligen Eingangswert (double zwischen -1 bis 5 Volt) aus, um A/D-Converter mit einschließlich nicht plausiblen Werten zu simulieren
    digital_value = random.randint(-1, 10)  # Range der Zahlen kann beliebig angepasst werden 
    print(digital_value)
    if digital_value < 0:                                                              # Prüfung des Messwerts auf Plausibilität
        digital_value = 0                                                              # Wenn Messwert nicht plausibel, wird auf 0 gesetzt
    return digital_value


def conv_process(shm_conv_log, shm_conv_stat,semaphore_conv_log, semaphore_conv_stat):
    
    SHM_SIZE = 1024
    
    # Start des Conv_process (Analog-Digital-Wandler und Shared Memory Schreiben)
    while True:
        # Daten vom Analog-Digital-Wandler erhalten und in den Shared Memory schreiben
        data = str(analog_to_digital_converter()).encode()
        
        # Daten in das Log-Prozess-Segment schreiben
        with mmap.mmap(shm_conv_log.fd, SHM_SIZE, access=mmap.ACCESS_WRITE) as mapfile:
            mapfile.seek(0)
            mapfile.write(data.ljust(SHM_SIZE))  # Daten schreiben und auffüllen
            mapfile.flush()
        semaphore_conv_log.release()  # Semaphore freigeben, um den Log-Prozess zu benachrichtigen
        
        # Daten in das Statistik-Prozess-Segment schreiben
        with mmap.mmap(shm_conv_stat.fd, SHM_SIZE, access=mmap.ACCESS_WRITE) as mapfile:
            mapfile.seek(0)
            mapfile.write(data.ljust(SHM_SIZE))  # Daten schreiben und auffüllen
            mapfile.flush()
        semaphore_conv_stat.release()  # Semaphore freigeben, um den Statistik-Prozess zu benachrichtigen
        # Kurze Pause, um den Datenfluss zu verlangsamen und die Ausgabe zu synchronisieren
        time.sleep(0.5)
        