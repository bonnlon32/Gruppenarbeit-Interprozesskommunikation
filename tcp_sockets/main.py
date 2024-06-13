#starten des gesamten prozesses
#fork noch einbauen
#signalhandler sigint noch einbauen
#fehlerhafte kommandozeilen eingaben abfangen!!

#---------------------------------------------------
import sys
import signal

# Signalhandler für SIGINT
def signal_handler(sig, frame):
    print("Programm wird beendet...")
    sys.exit(0)

# Registrieren des Signalhandlers für SIGINT
signal.signal(signal.SIGINT, signal_handler)

# Einfache Endlosschleife, um das Programm am Laufen zu halten
while True:
    pass


#----------------------------------------------------