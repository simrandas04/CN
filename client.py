import socket
import ssl
import time

# Server configuration
SERVER_HOST = '192.168.102.12'
SERVER_PORT = 5555

def send_position(client_socket, client_id, x, y):
    position_data = f"{client_id},{x},{y}"
    client_socket.send(position_data.encode('utf-8'))

def main():
    client_id = input("Enter client ID: ")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Wrap the socket with SSL
    client_socket = ssl.wrap_socket(client_socket, ssl_version=ssl.PROTOCOL_TLS)
    
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    
    while True:
        try:
            x = float(input("Enter X coordinate: "))
            y = float(input("Enter Y coordinate: "))
            send_position(client_socket, client_id, x, y)
            time.sleep(10)  # Send position every second
        except KeyboardInterrupt:
            print("\nExiting...")
            break

    client_socket.close()

if __name__ == "__main__":
    main()
