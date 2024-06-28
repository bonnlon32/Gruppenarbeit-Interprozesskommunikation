import time



def report_process(mqToReport):

    print("- - - REPORT-PROZESS\t GESTARTET - - -")

    while True:

        messageSum, priorität = mqToReport.receive()
        messageAvrg, priorität = mqToReport.receive()      # Empfangen der Nachricht, speichern der Prio sepperat

        messageSum = round(float(messageSum.decode()),2)            # Konvertierung von Byte zu String zu float und gerundet 2. Stelle
        messageAvrg = round(float(messageAvrg.decode()),2)          # Konvertierung von Byte zu String zu float und gerundet 2. Stelle

        print("REPORT - Summe: ", messageSum)              # Ausgabe
        print("REPORT - Mittelwert: ", messageAvrg)        # Ausgabe
        time.sleep(1)