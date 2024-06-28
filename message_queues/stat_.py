import time
#berechnet Mittelwert und Summe aus Conv


def stat_process(mqToReport, mqToStat):

    print("- - - STAT_-PROZESS\t GESTARTET - - -")

    avrg = 0.0
    sum = 0.0
    count = 0
    
    
    while True:

        message, priorität = mqToStat.receive()      # Empfangen der Nachricht, speichern der Prio sepperat
        num = float(message.decode())                # Konvertierung von Byte zu String zu float

        count+=1

        sum += num                                  # Berechnung Summe
        avrg = sum/count                            # Berechnung Mittelwert

        sumString = str(sum)
        avrgString = str(avrg)

        messageSum = sumString.encode()             # Konvertierung Nachricht in Bytes
        messageAvrg = avrgString.encode()
        mqToReport.send(messageSum)                 # Sendet Nachricht zu ReportSUM
        mqToReport.send(messageAvrg)                # Sendet Nachricht zu ReportAVRG

        time.sleep(1)