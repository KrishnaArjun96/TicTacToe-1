import socket
import sys


def encode(command):
    split = command.split(' ')
    print(split[0])
    
    if split[0] == 'place':
        command = 'PLACE '  + str(split[1])
    elif split[0] == 'exit': 
        command = 'EXIT'
    return command

def verify(message, sock):
    while message[0] == "Error":
        print(str(message[1]))
        command = raw_input(">:")
        encode(command)
        response = encode(command)
        sock.sendall(response)
        data = sock.recv(1024)
    	message = data.split(' : ')
        print(str(message[1]))

def help():
    print("login <userid> - logs user into the TicTacToe server")
    print("place <location> - makes move at location")
    print("exit - exits from game")


def main():

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #port_number = input("Enter the port:")
    #machine = input("Machine name:")

    # Connect the socket to the port where the server is listening
    sock.connect(('localhost', 8080))

    # logs in user in the format LOGIN <userid>

    userid = raw_input("Please log in:")
    command = "LOGIN " + userid + " "
    sock.send(command)

    # Connected to server response from the server
    connectionResponse = sock.recv(1024)
    print(connectionResponse)

    # Wait for the game to start
    board = sock.recv(1024)
    print(board)
    message = sock.recv(1024)
    print(message)

    # Start accepting commands from the player
    while True:
        
        command = raw_input(">:")
        while command == "help":
            help()
            command = raw_input(">:")
        request = encode(command)
        sock.send(request)
        print("Sent...")

        #Recieve message
        data = sock.recv(1024)
        print(data)
        

if __name__ == "__main__": main()
