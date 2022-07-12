import socket

def start_game(s, letter):
    name = input("Name: ")
    s.send(f"name = {name}".encode())
    family = input("Family: ")
    s.send(f"family = {family}".encode())
    city = input("City: ")
    s.send(f"city = {city}".encode())
    food = input("Food: ")
    s.send(f"food = {food}".encode())


def create_connection():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    port = 50000    
    s.connect(('127.0.0.1', port))
    return s, port

def print_help():
    print("Welcome!")
    print("Input start_game to Start the Game!")

def run_app():
    s, port = create_connection()
    print_help()
    server_msg = s.recv(1024)
    server_msg = server_msg.decode()
    command = input()
    while command is not None or server_msg is not None:
        if server_msg.startswith("Start Game With letter"):
            print(server_msg)
            letter = server_msg.split(" ")[4]
            start_game(s ,letter)
        if command == "start_game":
            s.send(command.encode())
        command = input()
    

