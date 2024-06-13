import socket
import struct 

def receive_integer(host='localhost', port=12345):
    # Erstelle einen TCP/IP-Socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    try:
        # Empfange Daten in Blöcken von 4 Bytes (da ein Integer 4 Bytes groß ist)
        data = client_socket.recv(4)
        if data:
            # Entpacke die empfangenen Bytes zu einem Integer
            received_integer = struct.unpack('!I', data)[0]
            print(f"Received integer: {received_integer}")
    finally:
        # Verbindung schließen
        client_socket.close()

if __name__ == "__main__":
    receive_integer()
