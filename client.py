import socket
import sys


def encode(command, addr):
    split = command.split(' ')
    if split[0] == 'place':
        command = 'PLACE '  + str(split[1]) + ' ' + str(addr)
    elif split[0] == 'exit': 
        command = 'EXIT ' + str(addr)
    else:
        command = 'HELP ' + str(addr)
    return command

def verify(message, sock, address):
    while message[0] == "Error":
        print(str(message[1]))
        command = input(">:")
        response = encode(command, address)
        sock.sendall(response)
        data = sock.recv(1024)
        message = data.split(' : ')
    print(str(message[1]))


def main():

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    port_number = input("Enter the port:")
    machine = input("Machine name:")

    # Connect the socket to the port where the server is listening
    sock.connect((machine, port_number))
    address = sock.recv(1024)

    # logs in user in the format LOGIN <userid>
    command = input("Please log in:")
    userid = command
    command = "LOGIN " + userid + " "
    sock.sendall(command)

    # server sends client its address tuple to store for future responses
    addr = sock.recv(1024)

    while True:
        
        #server sends message
        data = sock.recv(1024)
        message = data.split(' : ')
        verify(message, sock, address)


        #server sends message
        data = sock.recv(1024)
        message = data.split(' : ')
        verify(message, sock, address)
        
        if message[0] == "Message":
            command = input(">:")
            response = encode(command, address)
            sock.sendall(response)

        #server sends message
        data = sock.recv(1024)
        message = data.split(' : ')
        verify(message, sock, address)

        #server sends message
        data = sock.recv(1024)
        message = data.split(' : ')
        verify(message, sock, address)
        
        if message[0] == "Message":
            command = input(">:")
            response = encode(command, address)
            sock.sendall(response)


if __name__ == "__main__": main()
