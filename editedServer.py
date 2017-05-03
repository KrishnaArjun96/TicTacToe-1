#import socket module
from socket import *
import time
from serverMethods import *
from player import Player
from tictactoe import TicTacToe

serverSocket = socket(AF_INET, SOCK_STREAM)

#Prepare a sever socket
serverPort = 8080
serverSocket.bind(('',serverPort))
serverSocket.listen(2)
game = None

players = []

while True:
	#Establish the connection
	print('Welcome to TicTacToe')
	connectionSocket, addr =  serverSocket.accept()
	try:
		message =  connectionSocket.recv(8080)
		cmd = message.split(' ')
		# Contents of cmd are based on the options: LOGIN, HELP, PLACE or EXIT.

		if(cmd[0] == "LOGIN"):
			#cmd shall be as follows: LOGIN <usr_id>
			#The first user to login shall be placed first in the list and hence gets to go first with 'X'
			user_id = cmd[1]
			arrival_time = time.time()
			address = addr

			connectionSocket.sendto(str(addr), addr)

			p = None
			if(len(players) == 0):
				p = Player(user_id, arrival_time, address, 'X')
			else:
				p = Player(user_id, arrival_time, address, 'O')

			players.append(p)

			#Game starts only if the number of players is 2. 
			if(len(players) == 2):
				game = TicTacToe(players[0], players[1])
				respond_to_client(players[0], "Please make your move.", connectionSocket)
				respond_to_client(players[1], "Please wait for your turn.", connectionSocket)


	except IOError:
		#Send response message for file not found
		connectionSocket.send('HTTP/1.1 404 NOT FOUND!\r\n')	
		#Close client socket
		connectionSocket.close()
