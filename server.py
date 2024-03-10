import socket
import ssl
import threading

# Server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5555

USE_SSL = True
CERT_FILE = 'server.crt'

def handle_client(client_socket):
    while True:
        try:
            position_data = client_socket.recv(1024).decode('utf-8')
            client_socket.send(b'ACK')
        except ConnectionResetError:
            print("Client disconnected")
            break

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', SERVER_PORT))
    server.listen(5)

    print("[*] Server listening on port 5555")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()
