import Player
import Tictactoe
import select

# import socket module
from socket import *
import time

def find(user_id):
    for player in players:
        if(player.get_user_id() == user_id):
            return True
    return False

game = None
players = []

main_player = None
opponent = None

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setblocking(0)
# Prepare a sever socket
serverPort = 8080
serverSocket.bind(('localhost', serverPort))
serverSocket.listen(2)

# Declaring input sockets where we have to read
inputSocks = [ serverSocket ]

# Output sockets to which we have to write
outputSocks = []
otherList = []

while inputSocks:
    # Waiting for at least one of the sockets to be ready for processing
    readable, writable, exceptional = select.select(inputSocks, outputSocks, otherList)

    for socks in readable:

        if socks is serverSocket:
            connection, addr = serverSocket.accept()
            inputSocks.append(connection)

        else:
            # Recieve the data in existing sockets
            data = socks.recv(1024)
            cmd = data.split(' ')
            # This is where we have to handle various cases LOGIN, PLACE and EXIT
            if cmd[0] == 'LOGIN':
                user_id = cmd[1]
                if(find(user_id)):
                    socks.send("Error: " + user_id + " already in use. Try again.\n")
                else: 
                    arrival_time = time.time()
                    
                    p = None
                    if len(players) == 0:
                        p = Player.Player(user_id, arrival_time, socks, 'X')
                    else:
                        p = Player.Player(user_id, arrival_time, socks, 'O')

                    players.append(p)
                    socks.send("Welcome to TicTacToe!")

                if len(players) == 2:
                    game = Tictactoe.TicTacToe(players[0], players[1])

                    # Print board on each client.
                    game.get_player_one().get_address().send("\n\n" + players[0].get_user_id() + " and " + players[1].get_user_id() + " connected.\n" + game.print_board())
                    game.get_player_two().get_address().send("\n\n" + players[0].get_user_id() + " and " + players[1].get_user_id() + " connected.\n" + game.print_board())
                    game.get_player_one().get_address().send("\n\n Please make your move.")
                    game.get_player_two().get_address().send("\n\n Please wait for your turn.")

                    main_player = game.get_player_one()
                    opponent = game.get_player_two()

            elif cmd[0] == 'PLACE':
                # if socks != main_player.get_address():
                #     socks.send("Please wait for your turn")
                # else:
                if game.move(int(cmd[1]), main_player.get_char()):
                    game.inc_moves()
                    game_state = game.is_game_over(main_player.get_char())
                    if game.get_moves() == 9 and not game_state:
                        main_player.get_address().send(game.print_board() + "Game Over : Draw Game!")
                        opponent.get_address().send(game.print_board() + "Game Over : Draw Game!")

                    elif game_state:
                        main_player.get_address().send(game.print_board() + "Game Over : You lose!")
                        opponent.get_address().send(game.print_board() + "Game Over : You win!")
                            
                    else:
                        opponent.get_address().send(game.print_board() + "Please make your move.")
                        main_player.get_address().send(game.print_board() + "Please wait for your turn.")

                        temp = main_player
                        main_player = opponent
                        opponent = temp
                else:
                    socks.send("Invalid move!")

            elif cmd[0] == 'EXIT':
                opponent.set_status("Available")

                main_player.get_address().send("Game Over : Thank You for using this application.")
                opponent.get_address().send("Game Over : Your opponent exited the game.")

                # Removes from the list of players.
                # Removes from the game

serverSocket.close()
