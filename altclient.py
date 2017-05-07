import socket
import sys

def encode(command):
    split = command.split(' ')
    
    if not is_logged_in and split[0] == 'login':
        command = 'LOGIN ' + str(split[1])
    elif split[0] == 'place' and is_connected:
        command = 'PLACE '  + str(split[1])
    elif split[0] == 'exit' and is_connected: 
        command = 'EXIT'
    elif split[0] == 'help':
        command = 'HELP'
    elif not is_connected and is_logged_in and split[0] == 'play':
        command = 'PLAY '  + current_user + ' ' + str(split[1])
    elif is_logged_in and split[0] == 'who':
        command = 'WHO'
        command = "INVALID"
    return commands

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
    global current_user
    global is_connected 
    global is_logged_in

    is_connected = False
    is_logged_in = False

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #port_number = input("Enter the port:")
    #machine = input("Machine name:")

    # Connect the socket to the port where the server is listening
    sock.connect(('localhost', 8080))

    print("Connection Successful!")
    print(help())

    # logs in user in the format LOGIN <userid>

    # userid = raw_input("Please log in: ")
    # request = encode(command)
    # sock.send(command)

    # # Connected to server response from the server
    # connectionResponse = sock.recv(1024)
    # print(connectionResponse)

    # while "Error: " in connectionResponse:
    #     print(connectionResponse)
    #     userid = raw_input("Please log in: ")
    #     command = "LOGIN " + userid + " "
    #     sock.send(command)
    #     connectionResponse = sock.recv(1024)
    #     if(connectionResponse == "Welcome to TicTacToe!\n"):
    #         print(connectionResponse)
    #         break
    # command = raw_input(">:")
    # request = encode(command)
    # sock.send(request)
    
    # data = sock.recv(1024)
    # print(data)

    # # Wait for the game to start
    # message = sock.recv(1024)
    # print(message)

    # Start accepting commands from the player
    while True:

        # if " make " in message or "Invalid " in message:
        command = raw_input(">:")
        request = encode(command)
        while request == "INVALID" or request == "HELP":
            if request == "INVALID":
                command = raw_input(command + " is invalid.\n" + help() + "\n>:")
            else:
                command = raw_input(help() + "\n>:")
            request = encode(command)
        print(str(request))
        sock.send(request)

        #Recieve message
        data = sock.recv(1024)

        while "Error: " in data:
            print(data)
            command = raw_input(help() + "\n>:")
            request = encode(command)
            while request == "INVALID" or request == "HELP":
                if request == "INVALID":
                    command = raw_input(command + " is invalid.\n" + help() + "\n>:")
                else:
                    command = raw_input(help() + "\n>:")
                request = encode(command)
            sock.send(request)
            data = sock.recv(1024)

        if "login" in command:
            current_user = command.split(' ')[1]
            print(current_user + " has been successfully logged in.")
            is_logged_in = True

        if "play" in command:
            

        print(data)
        message = data
        if "Game Over" in data:
            break
        

if __name__ == "__main__": main()
