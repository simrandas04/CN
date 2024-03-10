import socket
import ssl
import time

# Server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5555

# SSL settings
USE_SSL = True
CERT_FILE = 'server.crt'

def send_position(client_socket, client_id, x, y):
    position_data = f"{client_id},{x},{y}"
    client_socket.send(position_data.encode('utf-8'))

def main():
    client_id = input("Enter client ID: ")

    if USE_SSL:
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_verify_locations(CERT_FILE)
        client_socket = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=SERVER_HOST)
    else:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((SERVER_HOST, SERVER_PORT))
    
    while True:
        try:
            x = float(input("Enter X coordinate: "))
            y = float(input("Enter Y coordinate: "))
            send_position(client_socket, client_id, x, y)

            # Receive acknowledgment or retransmission signal
            response = client_socket.recv(1024).decode('utf-8')
            if response == 'ACK':
                print("[*] Server acknowledgment received")
            elif response == 'RETRANSMIT':
                print("[*] Collision detected. Retransmitting position...")
                continue  # Skip the acknowledgment check after retransmission

            time.sleep(1)  # Send position every second
        except KeyboardInterrupt:
            print("\nExiting...")
            break

    client_socket.close()

if _name_ == "_main_":
    main()
