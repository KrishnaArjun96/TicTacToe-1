import socket
import sys


def help():
    print("login <name> : logs you into the server with user id <name>")
    print("place <n> : place piece in cell <n> if it is a valid move")
    print("exit : exits you from the game")


def main():
    # Create a TCP/IP socket
    print(str(socket.gethostbyname(socket.gethostname())))
    print(str(socket.gethostname()))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    port_number = input("Enter the port:")
    machine = input("Machine name:")

    # Connect the socket to the port where the server is listening
    sock.connect((machine, port_number))
    # address = sock.recv(1024)

    # logs in user in the format LOGIN <userid>
    command = input("Please log in:")
    userid = command
    command = "LOGIN " + userid + " "
    sock.sendall(command)

    # server sends client its address tuple to store for future responses
    addr = sock.recv(1024)

    while True:
        data = sock.recv(1024)
        print(str(data))

        # Still requires response interpretation
        # display updated board
        # respond appropriately
        command = input(">:")

        while command == "help":
            help()
            command = input(">:")
        if command == "EXIT":
            command = "EXIT " + userid
        else:
            split = command.split()
            command = split[0] + " " + split[1] + " " + "name " + userid
        print(command)
        sock.sendall(command)

if __name__ == "__main__": main()
