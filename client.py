import socket
import ssl
import time

# Server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5555
CLIENT_ID = input("Enter client ID: ")  # Prompt for client ID only in client script

# SSL settings
USE_SSL = True
CERT_FILE = 'server.crt'

def send_position(client_socket, x, y):
    position_data = f"{CLIENT_ID},{x},{y}"  # Use CLIENT_ID from global variable
    client_socket.send(position_data.encode('utf-8'))

def main():
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
            send_position(client_socket, x, y)

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

if __name__ == "__main__":
    main()
