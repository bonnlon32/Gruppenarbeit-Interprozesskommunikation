# # #starten des gesamten prozesses
# # #fork noch einbauen - als kommandozeileneingabe oder fork als duplizieren der prozesse?
# # #signalhandler sigint noch einbauen
# # #fehlerhafte kommandozeilen eingaben abfangen!!

# # import sys
# # import signal

# # # Signalhandler für SIGINT
# # #def signal_handler(sig, frame):
# #     print("Programm wird beendet...")
# #     sys.exit(0)

# # # Registrieren des Signalhandlers für SIGINT
# # signal.signal(signal.SIGINT, signal_handler)

# # # Einfache Endlosschleife, um das Programm am Laufen zu halten
# # while True:
# #     pass


#fork
import os
import time

def start_process(script_path):
    pid = os.fork()
    if pid == 0:  # Child process
        os.execvp('python3', ['python3', script_path])
    else:
        return pid

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    scripts = ['log.py', 'stats.py', 'report.py']
    processes = []

    for script in scripts:
        script_path = os.path.join(base_dir, script)
        if os.path.isfile(script_path):
            pid = start_process(script_path)
            processes.append(pid)
        else:
            print(f"Error: {script_path} not found")

    # Wartezeit um sicherzustellen, dass alle Serverprozesse laufen
    time.sleep(3)

    # Starte conv.py Prozess
    conv_script = os.path.join(base_dir, 'conv.py')
    if os.path.isfile(conv_script):
        pid = start_process(conv_script)
        processes.append(pid)
    else:
        print(f"Error: {conv_script} not found")

    # Optional, warte auf alle Prozesse
    for pid in processes:
        os.waitpid(pid, 0)

    print("All processes have finished.")

