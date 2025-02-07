import socket
import threading

# Fixed IP for the host PC
HOST_IP = 'enter your HOST ip here'
PORT = 12345
BUFFER_SIZE = 1024

def receive_messages(client):
    """Continuously listens for incoming messages from the server"""
    while True:
        try:
            message = client.recv(BUFFER_SIZE).decode()
            if not message:
                break
            print(f"\n{message}\n> ", end="")  # Display message without breaking input
        except:
            break

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST_IP, PORT))

    # Enter session code
    session_code = input("Enter the 4-digit session code: ")
    client.send(session_code.encode())

    # Wait for server response
    response = client.recv(BUFFER_SIZE).decode()
    if "Incorrect" in response:
        print(response)
        client.close()
        return

    # Enter username
    username = input("Enter your username: ")
    client.send(username.encode())

    # Start listening for messages
    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

    print("You can start chatting now! Type 'exit' to quit.")

    while True:
        message = input("> ")
        client.send(message.encode())

        if message.lower() == "exit":
            break

    client.close()

if __name__ == "__main__":
    start_client()
