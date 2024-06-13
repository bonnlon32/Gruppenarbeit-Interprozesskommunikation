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

# Konstanten für Host und Ports
HOST = '127.0.0.1'
CONV_PORT = 5001
LOG_PORT = 5002
STAT_PORT = 5003
REPORT_PORT = 5004

