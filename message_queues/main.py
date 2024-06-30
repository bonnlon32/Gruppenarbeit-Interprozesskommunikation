import os
import signal
import sys
import posix_ipc

# Das Prozessgerüst erstellt die Kindprozesse und enthält die Ressourcenfreigabe und Abbruchbedingung

#importiert die Prozesse
from conv import conv_process
from log import log_process
from report import report_process
from stat_ import stat_process

# Namen der MessageQueues
CONV_TO_LOG_QUEUE = "/conv_to_log_queue"
CONV_TO_STAT_QUEUE = "/conv_to_stat_queue"
STAT_TO_REPORT_QUEUE = "/stat_to_report_queue"


# Erstellung der Message Queues
mqToLog = posix_ipc.MessageQueue(CONV_TO_LOG_QUEUE, posix_ipc.O_CREAT)          #CONV_To_LOG
mqToStat = posix_ipc.MessageQueue(CONV_TO_STAT_QUEUE, posix_ipc.O_CREAT)        #CONV_To_STAT_
mqToReport = posix_ipc.MessageQueue(STAT_TO_REPORT_QUEUE, posix_ipc.O_CREAT)    #STAT_To_REPORT

child_pids = [] # Array um alle PIDs der Kindprozesse zu speichern -> für SignalHandler


def signal_handler(sig, frame):                 # Signal Handler für Ctrl + C Interrupt
    print("Signal zum Beenden empfangen")
    for pid in child_pids:
        os.kill(pid, signal.SIGTERM)            # Endet alle Forks/Kindprozesse
    mq_cleaner()                                # Entsorgt die MessageQueues
    print("Alle Kindprozesse wurden beendet")
    print("Elternprozess wird beendet")
    sys.exit(0)                                 # beendet Elternprozess

def mq_cleaner():                               # Schließt & leert die Message Queues
    mqList = [mqToLog, mqToStat, mqToReport]
    for i in range (len(mqList)):
        try:
            mqList[i].close()
            mqList[i].unlink()
        except:                                 # Sollte Message Queue nicht existieren, wird der Fehler aufgefangen
            pass
    print("Alle Queues geschlossen & gelöscht ")

if __name__ == "__main__":                  

    processes = [conv_process, log_process, report_process, stat_process] # Liste der Prozesse

    for i in range (len(processes)):            # Erstellt Kindprozesse mit Fork, bis alle gestartet sind
        # PID = Rückgabewert bei fork
        # -1 = fehlgeschlagen
        #  0 = Ich bin ein Kindprozess
        # >0 = Ich bin ein Elternprozess

        pid = os.fork()         # Fork um Kindprozess zu erstellen mit Rückgabewert=pid
        # Eltern&Kindprozess läuft ab hier als identische Kopie weiter, außer dass pid Wert unterschiedlich ist

        if pid == 0:            # Startet NUR im KINDPROZESS, wegen pid=0

            selected_process = processes[i]     # geht die Liste nacheinander durch, um die Funktionen zu starten

            # Startet Funktion mit Übergabe von Queues
            if (selected_process == conv_process):
                print("- - - CONV-PROZESS\t GESTARTET - - -")
                selected_process(mqToStat, mqToLog)
                
            elif(selected_process == log_process):
                print("- - - LOG-PROZESS\t GESTARTET - - -")
                selected_process(mqToLog)

            elif(selected_process == report_process):
                print("- - - REPORT-PROZESS\t GESTARTET - - -")
                selected_process(mqToReport)

            elif(selected_process == stat_process):
                print("- - - STAT_-PROZESS\t GESTARTET - - -")
                selected_process(mqToReport, mqToStat)


        elif pid > 0:                                               # Sollte nur in Elternprozess starten, da pid>0
            print("Kindprozess ",i+1," mit PID ", pid," gestartet")
            child_pids.append(pid)                                  # Speichert PID von Kindprozess in Array

        else:                                                       # Wenn Fork fehlschlägt (pid = -1)
            print("Fork für Kindprozess", i+1 ," Fehlgeschlagen")   
            for pid in child_pids:
                os.kill(pid, signal.SIGTERM)
            mq_cleaner()                                            # gibt Ressourcen frei
            print("!Beende Programm!")
            sys.exit(0)                                             # beendet Programm

    
    signal.signal(signal.SIGINT, signal_handler)                    # Aufruf SignalHandler

    for _ in range(len(processes)):                                 # wartet bis alle Kindprozesse geendet sind
        print("warte auf Beendung von Kindprozesse")                
        os.wait()      