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

def help():
    ret = "\n================================================================================\n"
    ret += 'Help: \n'
    ret += "\thelp - prints this menu.\n"
    ret += "\tlogin <userid> - logs user into the TicTacToe server.\n"
    ret += "\tplace <location> - makes move at location.\n"
    ret += "\texit - exits from game.\n"
    ret += "================================================================================\n"
    return ret


def main():

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print(help())

    machine = raw_input("Machine: ")
    port = raw_input("Port: ")

    # Connect the socket to the port where the server is listening
    sock.connect((machine, int(port)))

    # logs in user in the format LOGIN <userid>

    userid = raw_input("login ")
    command = "LOGIN " + userid
    sock.send(command)

    # Connected to server response from the server
    connectionResponse = sock.recv(1024)

    while "Error: " in connectionResponse:
        print(connectionResponse)
        userid = raw_input("login ")
        command = "LOGIN " + userid + " "
        sock.send(command)
        connectionResponse = sock.recv(1024)
        if(connectionResponse == "Welcome to TicTacToe!"):
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
