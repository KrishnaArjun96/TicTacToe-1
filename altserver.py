import player
import tictactoe
import select

# import socket module
from socket import *
import time

game = None
players = []

player = None
opponent = None

serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a sever socket
serverPort = 8080
serverSocket.bind(('localhost', serverPort))
serverSocket.listen(2)

print('Welcome to TicTacToe')

# Declaring input sockets where we have to read
inputSocks = [ serverSocket ]

# Output sockets to which we have to write
outputSocks = []
otherList = []

while inputSocks:
    # Waiting for at least one of the sockets to be ready for processing
    readable, writable, exceptional = select.select(inputSocks, outputSocks, otherList)

    for socks in readable:
        print("Reached here.")

        if socks is serverSocket:
            connection, addr = serverSocket.accept()
            inputSocks.append(connection)

        else:
            # Recieve the data in existing sockets
            data = socks.recv(1024)

            cmd = data.split(' ')
            # This is where we have to handle various cases LOGIN, PLACE and EXIT
            if cmd[0] is 'LOGIN':
                user_id = cmd[1]
                arrival_time = time.time()
                address = addr

                p = None
                if len(players) == 0:
                    p = player.Player(user_id, arrival_time, socks, 'X')
                else:
                    p = player.Player(user_id, arrival_time, socks, 'O')

                players.append(p)
                socks.send("Welcome to TicTacToe\n" + user_id+" is connected.\n")
                print("Welcome to TicTacToe\n" + user_id+" is connected.\n")

                if len(players) == 2:
                    print("Game Started")
                    game = tictactoe.TicTacToe(players[0], players[1])

                    # Print board on each client.
                    game.get_player_one().get_address().send(game.print_board())
                    game.get_player_two().get_address().send(game.print_board())
                    game.get_player_one().get_address().send("\n Please make your move.")
                    game.get_player_two().get_address().send("\n Please wait for your turn.")

                    player = game.get_player_one()
                    opponent = game.get_player_two()

            elif cmd[0] is 'PLACE':
                if socks != player.get_address():
                    player.get_address().send("Please wait for your turn")
                else:
                    if game.move(cmd[1], player.get_char()):
                        player.get_address().send(game.print_board())
                        print("Placed " + cmd[1] + ".")
                        opponent.get_address().send(game.print_board())
                        print(game.print_board() + "\n")

                        game_state = game.is_game_over(player.get_char())
                        if game_state:
                            player.get_address().send("GameOver : You lose!")
                            opponent.get_address().send("GameOver : You win!")
                            print("GameOver : You lose!\n")
                            print("GameOver : You win!\n")
                        else:
                            player.get_address().send("Wait for your turn")
                            opponent.get_address().send("Please play your turn")
                            temp = player
                            player = opponent
                            opponent = temp
                    else:
                        player.get_address().send("Invalid move!")

            elif cmd[0] is 'EXIT':
                opponent = game.get_opponent(cmd[1])
                opponent.set_status("Available")

                player.get_address().send("GameOver : Thank You for using this application.")
                player.get_address().send("GameOver : Your opponent exited the game.")

                # Removes from the list of players.
                # Removes from the game
                players.remove(player)
                if game.is_player_one(player):
                    game.set_player_one(None)
                if game.is_player_two(player):
                    game.set_player_two(None)


serverSocket.close()
