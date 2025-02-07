import socket
import random
import threading

# Fixed IP for the host PC
HOST_IP = 'enter your HOST ip here'
PORT = 12345
BUFFER_SIZE = 1024

clients = {}  # Stores client sockets with their usernames

def broadcast(message, sender_socket):
    """Send a message to all connected clients except the sender"""
    for client_socket, username in clients.items():
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode())
            except:
                client_socket.close()
                del clients[client_socket]

def handle_client(client_socket):
    """Handles communication with a client"""
    try:
        # Ask for the session code
        client_socket.send("Enter the 4-digit session code: ".encode())
        password = client_socket.recv(BUFFER_SIZE).decode()

        if password != str(session_code):
            client_socket.send("Incorrect code. Connection closed.".encode())
            client_socket.close()
            return

        # Ask for the username
        client_socket.send("Enter your username: ".encode())
        username = client_socket.recv(BUFFER_SIZE).decode().strip()

        # Store the client with its username
        clients[client_socket] = username
        print(f"{username} connected!")

        client_socket.send(f"Welcome, {username}! You can now chat.\n".encode())
        broadcast(f"{username} has joined the chat!", client_socket)

        while True:
            message = client_socket.recv(BUFFER_SIZE).decode()
            if message.lower() == "exit":
                break

            formatted_message = f"{username}: {message}"
            print(formatted_message)  # Display on the server console
            broadcast(formatted_message, client_socket)

    except:
        pass
    finally:
        print(f"{username} disconnected.")
        broadcast(f"{username} has left the chat.", client_socket)
        client_socket.close()
        del clients[client_socket]

def start_server():
    """Starts the chat server"""
    global session_code
    session_code = random.randint(1000, 9999)
    print(f"Session code: {session_code}")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST_IP, PORT))
    server.listen(5)
    print("Server is listening for connections...")

    while True:
        client_socket, client_address = server.accept()
        print(f"Connection from {client_address}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
