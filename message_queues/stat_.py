import time
import posix_ipc

# Dieser Prozess empfängt mittels MessageQueue Daten und errechnet Summe & Mittelwert. Schickt diese weiter an Report mittels MessageQueue

def stat_process(mqToReport, mqToStat):
    time.sleep(1)
    print("- - - STAT_-PROZESS\t GESTARTET - - -", flush=True)  # flush=True - verhindert Pufferung von Befehl - os.kill von Singalhandler ordentlich Prozess terminiert

    avrg = 0.0
    sum = 0.0
    count = 0.0
    
    try:
        while True:

            message, priorität = mqToStat.receive()              # Empfangen der Nachricht, speichern der Prio sepperat
            num = round(float(message.decode()),2)               # Konvertierung von Byte zu String zu float 

            count+=1

            sum += num                                           # Berechnung Summe
            avrg = round((sum/count),2)                          # Berechnung Mittelwert
            
            sum = round(sum,2)

            stringMessage = "REPORT - Summe: " + str(sum) + "\nREPORT Mittelwert: " + str(avrg)     # Konvertireung zu String

            messageEncoded = stringMessage.encode('utf-8')        # Konvertierung Nachricht in Bytes

            mqToReport.send(messageEncoded)                       # Sendet Nachricht zu ReportSUM

            time.sleep(1)

    except KeyboardInterrupt:
        pass