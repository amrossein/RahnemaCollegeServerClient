import random
import socket
import threading

total_clients = []


def start_game():
    letter = random.randint(65, 90)
    letter = chr(letter)
    for client in total_clients:
        client_s = client[0]
        client_s.send("Start Game With letter %s !", letter)


def handle_client(msg):
    if msg == "start_game":
        start_game()
    pass


def on_new_client(client_socket,addr):
    total_clients.append((client_socket, addr))
    while True:
        msg = client_socket.recv(1024)
        msg = msg.decode()
        handle_client(msg)
    client_socket.close()


def run_app(): 
    s = socket.socket()         # Create a socket object
    port = 50000                # Reserve a port for your service.

    print('Server started!')
    print('Waiting for clients...')

    s.bind(('127.0.0.1', port))        # Bind to the port
    s.listen(5)                 # Now wait for client connection.

    while True:
        c, addr = s.accept()     # Establish connection with client.
        print("New Connection established")
        t1 = threading.Thread(target=on_new_client, args=(c, addr))
        t1.start()
    
    s.close()

