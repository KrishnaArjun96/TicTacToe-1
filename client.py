import socket
import sys


def encode(command):
    split = command.split(' ')
    
    if split[0] == 'place':
        command = 'PLACE '  + str(split[1])
    elif split[0] == 'exit': 
        command = 'EXIT'
    elif split[0] == 'help':
        command = 'HELP'
    else:
        command = "INVALID"
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
    ret = 'Help: \n'
    ret += "login <userid> - logs user into the TicTacToe server.\n"
    ret += "place <location> - makes move at location.\n"
    ret += "exit - exits from game.\n"
    ret += "games - lists ongoing games.\n"
    ret += "who - lists players who are currently logged in and available to play.\n"
    ret += "play <userid> - starts a game with player userid if they are available.\n"
    return ret


def main():

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #port_number = input("Enter the port:")
    #machine = input("Machine name:")

    machine = raw_input("Machine: ")
    port = input("Port: ")

    # Connect the socket to the port where the server is listening
    sock.connect((machine, port))

    # logs in user in the format LOGIN <userid>

    userid = raw_input("Please log in: ")
    command = "LOGIN " + userid + " "
    sock.send(command)

    # Connected to server response from the server
    connectionResponse = sock.recv(1024)

    while "Error: " in connectionResponse:
        print(connectionResponse)
        userid = raw_input("Please log in: ")
        command = "LOGIN " + userid + " "
        sock.send(command)
        connectionResponse = sock.recv(1024)
        if(connectionResponse == "Welcome to TicTacToe!\n"):
            break

    print(connectionResponse)

    # Wait for the game to start
    message = sock.recv(1024)
    print(message)

    # Start accepting commands from the player
    while True:

        if " make " in message or "Invalid " in message:
            command = raw_input(">:")
            request = encode(command)
            while request == "INVALID" or request == "HELP":
                if request == "INVALID":
                    command = raw_input(command + " is invalid.\n" + help() + "\n>:")
                else:
                    command = raw_input(help() + "\n>:")
                request = encode(command)
            sock.send(request)

        #Recieve message
        data = sock.recv(1024)
        print(data)
        message = data
        if "Game Over" in data:
            break
        

if __name__ == "__main__": main()
