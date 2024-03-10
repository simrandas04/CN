import socket
import ssl
import time

# Server configuration
SERVER_HOST = '10.1.21.33'
SERVER_PORT = 5555

def send_position(client_socket, client_id, x, y):
    position_data = f"{client_id},{x},{y}"
    client_socket.send(position_data.encode('utf-8'))

def main():
    client_id = input("Enter client ID: ")

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Wrap the socket with SSL/TLS
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    client_socket_ssl = context.wrap_socket(client_socket, server_hostname=SERVER_HOST)

    # Connect to the server
    client_socket_ssl.connect((SERVER_HOST, SERVER_PORT))
    
    try:
        while True:
            x = float(input("Enter X coordinate: "))
            y = float(input("Enter Y coordinate: "))
            send_position(client_socket_ssl, client_id, x, y)
            time.sleep(1)  # Send position every second
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        # Close the SSL socket
        client_socket_ssl.close()

if _name_ == "_main_":
    main()
