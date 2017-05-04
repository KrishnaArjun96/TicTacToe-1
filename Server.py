import player
import tictactoe
import select

# import socket module
from socket import *
import time

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
            print(data)
            cmd = data.split(' ')
            # This is where we have to handle various cases LOGIN, PLACE and EXIT
            if cmd[0] == 'LOGIN':
                print("here")
                user_id = cmd[1]
                arrival_time = time.time()
                
                p = None
                if len(players) == 0:
                    p = player.Player(user_id, arrival_time, socks, 'X')
                else:
                    p = player.Player(user_id, arrival_time, socks, 'O')

                players.append(p)
                socks.send("Welcome to TicTacToe\n")
                print(user_id+ "is connected.\n")

                if len(players) == 2:
                    print("Game Started")
                    game = tictactoe.TicTacToe(players[0], players[1])

                    # Print board on each client.
                    game.get_player_one().get_address().send(game.print_board())
                    game.get_player_two().get_address().send(game.print_board())
                    game.get_player_one().get_address().send("\n Please make your move.")
                    game.get_player_two().get_address().send("\n Please wait for your turn.")

                    main_player = game.get_player_one()
                    opponent = game.get_player_two()

            elif cmd[0] == 'PLACE':
                if socks != main_player.get_address():
                    socks.send("Please wait for your turn")
                else:
                    if game.move(int(cmd[1]), main_player.get_char()):
                        socks.send(game.print_board())
                        print("Placed " + cmd[1] + ".")
                        opponent.get_address().send(game.print_board())
                        print(game.print_board() + "\n")

                        game_state = game.is_game_over(main_player.get_char())
                        if game_state:
                            socks.send("GameOver : You lose!")
                            opponent.get_address().send("GameOver : You win!")
                            
                        else:
                            socks.send("Wait for your turn")
                            opponent.get_address().send("Please play your turn")

                    else:
                        socks.send("Invalid move!")

            elif cmd[0] == 'EXIT':
                opponent = game.get_opponent(cmd[1])
                opponent.set_status("Available")

                main_player.get_address().send("GameOver : Thank You for using this application.")
                main_player.get_address().send("GameOver : Your opponent exited the game.")

                # Removes from the list of players.
                # Removes from the game
                players.remove(main_player)
                if game.is_player_one(main_player):
                    game.set_player_one(None)
                if game.is_player_two(main_player):
                    game.set_player_two(None)


serverSocket.close()
