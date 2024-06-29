import os
import signal
import sys
import posix_ipc

#importiert die Prozesse
from conv import conv_process
from log import log_process
from report import report_process
from stat_ import stat_process

#Namen der MessageQueues
CONV_TO_LOG_QUEUE = "/conv_to_log_queue"
CONV_TO_STAT_QUEUE = "/conv_to_stat_queue"
STAT_TO_REPORT_QUEUE = "/stat_to_report_queue"


# Erstellung der MessageQueue und Einstellung der Attribute
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
    sys.exit(0)                                 # beendet main

def mq_cleaner():                       # Leert und schließt die MessageQueues
    mq_flush(mqToLog)
    mq_flush(mqToStat)
    mq_flush(mqToReport)
    mqToLog.close()                     # Schließt alle Queues
    mqToStat.close()                    
    mqToReport.close()
    mqToLog.unlink()                    # Löscht alle Queues
    mqToStat.unlink()
    mqToReport.unlink()
    print("Alle Queues Flushed & Closed & Deleted ")


def mq_flush(mq):                       # Leert die MessageQueues
    while True:
        try:
            mq.receive(timeout=0)       # Empfängt Nachricht, aber blockiert nicht
        except posix_ipc.BusyError:
            break                       # Wenn keine Nachrichten mehr, beendet Schleife
        except posix_ipc.Error as e:
            print("Fehler beim Flush der Message Queue")
            break

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

            selected_process = processes[i]                 # geht die Liste nacheinander durch, um die Funktionen zu starten

            # Startet Funktion mit Übergabe von Queues
            if (selected_process == conv_process):
                selected_process(mqToStat, mqToLog)
            elif(selected_process == log_process):
                selected_process(mqToLog)
            elif(selected_process == report_process):
                selected_process(mqToReport)
            elif(selected_process == stat_process):
                selected_process(mqToReport, mqToStat)


        elif pid > 0:                                               # Sollte nur in Elernprozess starten, da pid>0
            print("Kindprozess ",i+1," mit PID ",pid," gestartet")  # Gibt Status aus
            child_pids.append(pid)                                  # Speichert PID von Kindprozess in Array

        else:                                                       # Wenn Fork fehlschlägt (pid = -1)
            print("Fork für Kindprozess", i+1 ," Fehlgeschlagen")   
            sys.exit(1)                                             # beendet Programm

    signal.signal(signal.SIGINT, signal_handler)                    # Aufruf SignalHandler

    for _ in range(len(processes)):                                 # wartet bis alle Kindprozesse geendet sind, damit signalHandler funktioniert und main weiter läuft
        print("warte auf Beendung von Kindprozesse")
        os.wait()                       
     