import socket
import struct

def start_server(host='localhost', port=12345, noahs_zahl=0):  #def ist methode mit 2 parameter
    # Erstelle einen TCP/IP-Socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    while True:
        # Warte auf eine Verbindung
        connection, client_address = server_socket.accept()
        try:
            print(f"Connection from {client_address}")

            # Der Float, den wir senden wollen
            float_to_send = noahs_zahl
            # Packe den Float in 4 Bytes (Big Endian)
            packed_data = struct.pack('!I', float_to_send)
            # Sende die gepackten Daten
            connection.sendall(packed_data)
            print(f"Sent float: {float_to_send}")

        finally:
            # Verbindung schließen
            connection.close()

if __name__ == "__main__":
    start_server(noahs_zahl=3)
