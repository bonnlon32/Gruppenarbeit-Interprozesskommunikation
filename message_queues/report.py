import time
import posix_ipc

# Dieser Enlosprozess empfängt Daten mittels MessageQueue aus Stat_ und gibt diese in der Shell aus

def report_process(mqToReport):
    time.sleep(1)
    print("- - - REPORT-PROZESS\t GESTARTET - - -", flush=True)         # flush=True - verhindert Pufferung von Befehl - os.kill von Singalhandler ordentlich Prozess terminiert
    try:
        while True:

            message, priorität = mqToReport.receive()                   # Empfangen der Nachricht, speichern der Prio sepperat
            messageDecoded = message.decode('utf-8')                    # Konvertierung von Byte zu String 
            print(messageDecoded)                                       # Ausgabe
            time.sleep(1)
    except KeyboardInterrupt:
        pass