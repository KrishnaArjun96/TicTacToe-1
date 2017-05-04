import player
import tictactoe

# import socket module
from socket import *
import time


def respond_to_client(player, message):
    connectionSocket.sendTo(message, player.get_address)


def get_player(address):
    for player in players:
        if player.get_address == address:
            return player
    return None


def print_help():
    ret = 'Help Menu:\n' + 'HELP:\t\tPrints this menu.\n'
    ret += 'LOGIN <urs_id>:\tConnect to the server using the unique user id.\n'
    ret += 'PLACE <position>:\tIssues a new move and the piece is placed at the position in an array.\n'
    ret += 'EXIT:\t\tExits and disconnects.'
    return ret


serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a sever socket
serverPort = 8080
serverSocket.bind(('', serverPort))
serverSocket.listen(2)
game = None

players = []

while True:
    # Establish the connection
    print('Welcome to TicTacToe')
    # addr : stores the address of the client.
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(8080)
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
                p = player.Player(user_id, arrival_time, address, 'X')
            else:
                p = player.Player(user_id, arrival_time, address, 'O')

            players.append(p)
            respond_to_client("Address : " + str(addr), addr)

            # Game starts only if the number of players is 2.
            if len(players) == 2:
                game = tictactoe.TicTacToe(players[0], players[1])
                # Print board on each client.
                connectionSocket.sendall(game.print_board())
                respond_to_client(players[0], "Message : Please make your move.")
                respond_to_client(players[1], "Error : Please wait for your turn.")

        elif cmd[0] == "PLACE":
            # cmd shall be as follows: PLACE <location> <usr_address>.
            if cmd[2] != game.get_turn():
                # If it is not the correct user, send appropriate message.
                # The variable turn stores the address of the user who is supposed to play.
                connectionSocket.sendTo("Message : Please wait for your turn.", cmd[2])
            else:
                # Allows the user to make the move.
                player = get_player(cmd[2])
                if game.move(cmd[1], player.get_char()):
                    # Checks if the Game is OVER. Prints necessary messages if true.
                    connectionSocket.sendall(game.print_board())
                    game_state = game.is_game_over(player.get_char())
                    if game_state:
                        connectionSocket.sendTo("GameOver : You lose!", cmd[2])
                        opponent = game.get_opponent(cmd[2])
                        respond_to_client(opponent, "GameOver : You win!")
                else:
                    connectionSocket.sendTo("Error : Move not possible. Position " + cmd[1] + " occupied.", cmd[2])
                # Updates the game board to all users.
                connectionSocket.sendAll(game.get_board())

        elif cmd[0] == "EXIT":
            # cmd shall be as follows: EXIT <usr_address>.
            player = get_player(cmd[1])

            # Sets status of opponent to 'Available'
            opponent = game.get_opponent(cmd[1])
            opponent.set_status("Available")

            respond_to_client(player, "GameOver : Thank You for using this application.")
            respond_to_client(opponent, "GameOver : Your opponent exited the game.")

            # Removes from the list of players.
            # Removes from the game
            players.remove(player)
            if game.is_player_one(player):
                game.set_player_one(None)
            if game.is_player_two(player):
                game.set_player_two(None)

        elif cmd[0] == "HELP":
            # cmd shall be as follows: HELP <usr_address>.
            # Prints the help menu.
            player = get_player(cmd[1])
            respond_to_client(player, print_help())


    except IOError:
        # Send response message for file not found
        connectionSocket.send('HTTP/1.1 404 NOT FOUND!\r\n')
        # Close client socket
        connectionSocket.close()

    serverSocket.close()
