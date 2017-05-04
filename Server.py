import player
import tictactoe

# import socket module
from socket import *
import time


def get_player(address):
    for player in players:
        if player.get_address == address:
            return player
    return None


serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a sever socket
serverPort = 8080
serverSocket.bind(('localhost', serverPort))
serverSocket.listen(2)

print('Welcome to TicTacToe')
    
cPlayer = None
game = None

players = []

while True:
    # Establish the connection
    # addr : stores the address of the client.
    if(len(players) != 2):
        connectionSocket, addr = serverSocket.accept()

    try:
        message = connectionSocket.recv(8080)
        print("HELLO..." + str(message))
        cmd = message.split(' ')
        # Contents of cmd are based on the options: LOGIN, HELP, PLACE or EXIT.

        if cmd[0] == "LOGIN":
            # cmd shall be as follows: LOGIN <usr_id>.
            # The first user to login shall be placed first in the list and hence gets to go first with 'X'
            user_id = cmd[1]
            arrival_time = time.time()
            address = addr

            p = None
            if len(players) == 0:
                p = player.Player(user_id, arrival_time, connectionSocket, 'X')
            else:
                p = player.Player(user_id, arrival_time, connectionSocket, 'O')

            players.append(p)
            p.get_address().send("Connected to Server")
            
            print(user_id+" has connected")

            # Game starts only if the number of players is 2.
            if len(players) == 2:
                print("game started")
                game = tictactoe.TicTacToe(players[0], players[1])

                cPlayer = players[0]
                
                # Print board on each client.
                print(game.print_board())
                game.get_player_one().get_address().send(game.print_board())
                game.get_player_two().get_address().send(game.print_board())
                game.get_player_one().get_address().send("\n Please make your move.")
                game.get_player_two().get_address().send("\n Please wait for your turn.")

        elif cmd[0] == "PLACE":

            if cPlayer.get_address() != connectionSocket:
                connectionSocket.sendto("Please wait for your turn")

            
            else:
                # Allows the user to make the move.
                player = cPlayer

                opponent = game.get_player_one
                if(game.get_player_one() == cPlayer):
                    opponent = game.get_player_two()

                if game.move(cmd[1], player.get_char()):
                    # Checks if the Game is OVER. Prints necessary messages if true.
                    game.get_player_one().get_address().send(game.print_board())
                    game.get_player_two().get_address().send(game.print_board())
                    
                    game_state = game.is_game_over(player.get_char())
                    print(game_state)

                    if game_state:
                        player.get_address().send("GameOver : You lose!")
                        opponent.get_address().send("GameOver : You win!")
                    else:
                        player.get_address().send("Wait for your turn")
                        opponent.get_address().send("Please play your turn")
                        cPlayer = opponent
                else:
                    player.get_address().send("Invalid move!")
                
        elif cmd[0] == "EXIT":
            # cmd shall be as follows: EXIT <usr_address>.
            player = get_player(cmd[1])

            # Sets status of opponent to 'Available'
            opponent = game.get_opponent(cmd[1])
            opponent.set_status("Available")
            
            connectionSocket.sendto("GameOver : Thank You for using this application.", player.get_address())
            connectionSocket.sendto("GameOver : Your opponent exited the game.", opponent.get_address())

            # Removes from the list of players.
            # Removes from the game
            players.remove(player)
            if game.is_player_one(player):
                game.set_player_one(None)
            if game.is_player_two(player):
                game.set_player_two(None)


    except IOError:
        # Send response message for file not found
        connectionSocket.send('HTTP/1.1 404 NOT FOUND!\r\n')
        # Close client socket
        connectionSocket.close()


serverSocket.close()
