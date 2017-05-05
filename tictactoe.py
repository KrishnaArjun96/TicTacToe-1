import player


# This is the main game class, which has two players 1 and 2.
class TicTacToe:
    # Constructors.
    def __init__(self, player_one, player_two):
        self.board = ['.', '.', '.', '.', '.', '.', '.', '.', '.']
        self.player_one = player_one
        self.player_two = player_two
        self.player_one.set_status("Busy")
        self.player_two.set_status("Busy")
        self.turn = self.player_one.get_address()

    # Getters and setters.
    def get_player_one(self):
        return self.player_one

    def get_player_two(self):
        return self.player_two

    def set_player_one(self, player):
        self.player_one = player

    def set_player_two(self, player):
        self.player_two = player

    def is_player_one(self, player):
        if (self.player_one == player):
            return True
        return False

    def is_player_two(self, player):
        if self.player_two == player:
            return True
        return False

    def get_player(self, addr):
        if self.player_one.get_address == addr:
            return self.player_one
        return self.player_two

    def get_opponent(self, addr):
        if self.player_one.get_address == addr:
            return self.player_two
        return self.player_one

    def get_turn(self):
        return self.turn

    def set_turn(self, turn):
        self.turn = turn

    def print_board(self):
        ret = 'Board : \n'
        i = 0
        j = 0
        while j<9:
            if i == 3:
                ret += '\n'
                i = 0
            i += 1
            ret += str(self.board[j]) + ' '
            j += 1
        return ret + '\n'

    # This method positions the character 'O' or 'X' at the position in the board.
    # This also checks if the position the user wants to enter the char is free or not.
    # returns true if successful, or false.
    def move(self, position, char):
        if self.board[position] != '.':
            return False
        self.board[position] = char
        return True

    def get_board(self):
        return self.board

    # Checks if the user loses.
    # Three in a row, three in a column and the diagonals are checked in this method.
    def is_game_over(self, char):
        # Checks for Three in a column.
        i = 0
        while i < 3:
            if self.board[i] == char and self.board[i + 3] == char and self.board[i + 6] == char:
                return True
            i += 1

        # Checks for Three in a row.
        i = 0
        while i < 9:
            if self.board[i] == char and self.board[i + 1] == char and self.board[i + 2] == char:
                return True
            i += 3

        # Checks for main diagonal
        if self.board[0] == char and self.board[4] == char and self.board[8] == char:
            return True

        # Checks for the other diagonal
        if self.board[2] == char and self.board[4] == char and self.board[6] == char:
            return True

        return False
