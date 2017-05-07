import player
import tictactoe
import select

# import socket module
from socket import *
import time

def find(user_id):
    if get_player(user_id) == None:
        return False
    return True

def get_player(user_id):
    for player in players:
        if(player.get_user_id() == user_id):
            return player
    return None

def get_player_socket(socket):
    for player in players:
        if(player.get_address == socket):
            return player
    return None

def list_players():
    ret = 'PLAYERS:\n'
    for player in players:
        ret += '\t' + player.get_user_id() + '\n'
    return ret

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
                    
                    p = player.Player(user_id, arrival_time, socks, '-')

                    players.append(p)
                    socks.send("Connected to TicTacToe!\n")

            elif cmd[0] == 'PLAY':
                if len(players) >= 2:
                    p1 = get_player(cmd[1])
                    p2 = get_player(cmd[2])
                    p1.get_address().send("Waiting for " + cmd[2] + " to connect.\n")
                    check = socks.recv(1024)
                    print(str(checks))
                    if(check == "yes"):
                        if(p1.get_arrival_time() > p2.get_arrival_time()):
                            main_player = p1
                            opponent = p2
                        else: 
                            main_player = p2
                            opponent = p1
                        main_player.set_char('X')
                        opponent.set_char('O')
                        game = tictactoe.TicTacToe(main_player, opponent)

                        game.get_player_one().get_address().send("Successfully connected.\n")
                        game.get_player_two().get_address().send("Successfully connected.\n")

                        # Print board on each client.
                        game.get_player_one().get_address().send(game.print_board() + "\n Please make your move.")
                        game.get_player_two().get_address().send(game.print_board() + "\n Please wait for your turn.")
                    else:
                        p1.get_address().send(cmd[2] + " refused to connect.\n")

            elif cmd[0] == 'WHO':
                socks.send(list_players())

            elif cmd[0] == 'PLACE':
                if game.move((int(cmd[1])-1), main_player.get_char()):
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
                    socks.send("Error: Invalid move!")

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
