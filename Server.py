#import socket module
from socket import *
import time
import player
import tictactoe

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

		if(cmd[0] == "LOGIN"):
			user_id = cmd[1]
			arrival_time = time.time()
			address = cmd[2]

			p = None
			if(len(players) == 0):
				p = Player(user_id, arrival_time, address, 'X')
			else:
				p = Player(user_id, arrival_time, address, 'O')

			players.append(p)

			if(len(players) == 2):
				game = TicTacToe(players[0], players[1])
				respond_to_client(players[0], "Please make your move.")
				respond_to_client(players[1], "Please wait for your turn.")
		
		elif(cmd[0] == "PLACE"):
			if(cmd[2] != game.get_turn()):
				connectionSocket.sendTo("Please wait for your turn.", cmd[2])
			else:
				player = get_player(cmd[2])
				if(game.move(cmd[1], player.get_char())):
					game_state = game.is_game_over()
					if(game_state):
						connectionSocket.sendTo("You lose!", cmd[2])
						opponent = game.get_opponent(cmd[2]);
						respond_to_client(opponent, "You win!")
					connectionSocket.sendAll(game.get_board())

		elif(cmd[0] == "EXIT"):
			player = get_player(cmd[1])
			opponent = game.get_opponent(cmd[1])
			opponent.set_status("Available")
			respond_to_client(player, "Thank You for using this application.")
			respond_to_client(opponent, "Your opponent exited the game.")
			players.remove(player)
			if(game.is_player_one(player)):
				game.set_player_one(None)
			if(game.is_player_two(player)):
				game.set_player_two(None)

		elif(cmd[0] == "HELP"):
			player = get_player(cmd[1])
			respond_to_client(player, print_help())
			players.remove(player)

		else:
			#error message.

	except IOError:
		#Send response message for file not found
		connectionSocket.send('HTTP/1.1 404 NOT FOUND!\r\n')	
		#Close client socket
		connectionSocket.close()
serverSocket.close() 

def respond_to_client(player, message):
	connectionSocket.sendTo(message, player.get_address)

def get_player(address):
	for player in players:
		if(player.get_address == address):
			return player
	return None

def print_help():
	ret = 'Help Menu:\n' + 'HELP:\t\tPrints this menu.\n' + 'LOGIN <urs_id>:\tConnect to the server using the unique user id.\n'
	ret = ret + 'PLACE <position>:\tIssues a new move and the peice is placed at the position in an array.\n' + 'EXIT:\t\tExits and disconnects.'
