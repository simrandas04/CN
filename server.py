import socket
import ssl
import threading

# Server configuration
SERVER_HOST = '192.168.102.12'
SERVER_PORT = 5555

# Dictionary to store client positions
client_positions = {}

def handle_client(client_socket):
    while True:
        try:
            # Receive position data from client
            position_data = client_socket.recv(1024).decode('utf-8')
            client_id, x, y = position_data.split(',')
            client_positions[client_id] = (float(x), float(y))
            
            # Check for collisions
            for client1, pos1 in client_positions.items():
                for client2, pos2 in client_positions.items():
                    if client1 != client2:
                        if abs(pos1[0] - pos2[0]) < 10 and abs(pos1[1] - pos2[1]) < 10:
                            collision_message = f"Collision detected between {client1} and {client2}"
                            print(collision_message)  # Print for server console
                            client_socket.send(collision_message.encode('utf-8'))
        except Exception as e:
            print(f"Error: {e}")
            break

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Wrap the server socket with SSL
    server_socket = ssl.wrap_socket(server_socket, certfile='cert.pem', keyfile='key.pem', server_side=True)
    
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"[*] Listening on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"[*] Accepted connection from {client_address[0]}:{client_address[1]}")
        
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
