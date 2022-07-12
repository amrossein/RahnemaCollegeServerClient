import random
import socket
import threading

total_clients = []
names = {}
families = {}
cities = {}
foods = {}
clients_to_score = {}

fields = [names, families, cities, foods]


def end_game():
    for field in fields:
        for key in field.keys():
            if (len(field[key]) == 1):
                score = clients_to_score[field[key][1]]
                score += 10
                clients_to_score[field[key][1]] = score
            else:
                for socket in field[key]:
                    score = clients_to_score[socket]
                    score += 5
                    clients_to_score[socket] = score
    

def start_game():
    letter = random.randint(65, 90)
    letter = chr(letter)
    for client in total_clients:
        client_s = client[0]
        client_s.send("Start Game With letter %s !", letter)


def handle_client(client_socket, msg: str):
    if msg == "start_game":
        start_game()
    elif msg.startswith("name = "):
        name = msg.split(" ")[2]
        if name not in names:
            names[name] = [client_socket]
        else:
            names[names].append(client_socket)
    elif msg.startswith("family = "):
        family = msg.split(" ")[2]
        if family not in families:
            families[family] = [client_socket]
        else:
            families[family].append(client_socket)
    elif msg.startswith("city = "):
        city = msg.split(" ")[2]
        if city not in cities:
            cities[city] = [client_socket]
        else:
            cities[city].append(client_socket)
    elif msg.startswith("food = "):
        food = msg.split(" ")[2]
        if food not in foods:
            foods[food] = [client_socket]
        else:
            foods[food].append(client_socket)


def on_new_client(client_socket,addr):
    total_clients.append((client_socket, addr))
    clients_to_score[client_socket] = 0
    while True:
        msg = client_socket.recv(1024)
        msg = msg.decode()
        print(msg)
        handle_client(client_socket, msg)
    client_socket.close()


def run_app(): 
    s = socket.socket()                      # Create a socket object
    port = 1233                              # Reserve a port for your service.

    print('Server started!')
    print('Waiting for clients...')

    s.bind(('127.0.0.1', port))              # Bind to the port
    s.listen(5)                              # Now wait for client connection.

    while True:
        c, addr = s.accept()                 # Establish connection with client.
        print("New Connection established")
        t1 = threading.Thread(target=on_new_client, args=(c, addr))
        t1.start()
    
    s.close()

