import socket
import sys

def help():
	print("login <name> : logs you into the server with user id <name>")
	print("place <n> : place piece in cell <n> if it is a valid move")
	print("exit : exits you from the game")

def parse(arg):
	split = arg.split()
	command = split[0] + ":" + arg[1]
	return command

def interpret(command):


def main():
	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	port_number = input("Enter the port:")
	machine = input("Machine name:")

	# Connect the socket to the port where the server is listening
	sock.create_connection((machine, port_number))

	command = input("Please log in:")
	split = command.split()
	command = split[0] + ":" + arg[1]
	userid = split[1]
	sock.sendall(command)
	
	while True:
		data = sock.recv(1024)
		#interpret data
		#display board
		#respond appropriately
		command = input(">:")
		command = interpret(command)
		sock.sendall(command)


if __name__ == "__main__": main()
