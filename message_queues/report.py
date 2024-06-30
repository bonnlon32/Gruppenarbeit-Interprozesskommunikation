import time

# Dieser Enlosprozess empfängt Daten mittels MessageQueue aus Stat_ und gibt diese in der Shell aus

def report_process(mqToReport):
    time.sleep(1)

    while True:

        message, priority = mqToReport.receive()                   # Empfangen der Nachricht, speichern der Prio sepperat
        messageDecoded = message.decode('utf-8')                    # Konvertierung von Byte zu String 
        print(messageDecoded)                                       # Ausgabe
        time.sleep(1)