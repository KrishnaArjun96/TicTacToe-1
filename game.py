class Game(object):

	board = ['.', '.', '.', '.', '.', '.', '.', '.', '.']
	winner = None
	over = False

	def __init__(self, one, two):
		self.one = one
		self.two = two
		self.turn = one

	def printBoard(self):
		print('{0} {1} {2}'.format(self.board[0], self.board[1], self.board[2]))
		print('{0} {1} {2}'.format(self.board[3], self.board[4], self.board[5]))
		print('{0} {1} {2}'.format(self.board[6], self.board[7], self.board[8]))
		
	def place(self, player, location):
		if self.getTurn() != player:
			print('It is not your turn')
			return  False
		if location < 1 or location > 9 or self.board[location - 1] != '.':
			print('Invalid move')
			return False
		self.board[location - 1] = player.getPiece()
		if self.getTurn() == self.one:
			self.setTurn(self.two)
		else:
			self.setTurn(self.one)
		return True

	def getTurn(self):
		return self.turn

	def setTurn(self, player):
		self.turn = player

	def isOver(self):
		over = False
		winner = ' '


		if self.board[0] == 'X' and self.board[1] == 'X' and self.board[2] == 'X':
			over = True;
			winner = 'X'
		elif board[3] == 'X' and board[4] == 'X' and board[5] == 'X':
			over = True;
			winner = 'X'
		elif board[6] == 'X' and board[7] == 'X' and board[8] == 'X':
			over = True
			winner = 'X'
		elif board[0] == 'X' and board[4] == 'X' and board[8] == 'X':
			over = True
			winner = 'X'
		elif board[2] == 'X' and board[4] == 'X' and board[6] == 'X':
			over = True
			winner = 'X'
		elif board[0] == 'O' and board[1] == 'O' and board[2] == 'O':
			over = True;
			winner = 'O'
		elif board[3] == 'O' and board[4] == 'O' and board[5] == 'O':
			over = True;
			winner = 'O'
		elif board[6] == 'O' and board[7] == 'O' and board[8] == 'O':
			over = True
			winner = 'O'
		elif board[0] == 'O' and board[4] == 'O' and board[8] == 'O':
			over = True
			winner = 'O'
		elif board[2] == 'O' and board[4] == 'O' and board[6] == 'O':
			over = True
			winner = 'O'
		else:
			over = False
		if over and  winner == 'X':
			if self.one.getPiece() == 'X':
				winner = self.one
				over = True
			else:
				winner = self.two
				over = True
		elif over and winner == 'O':
			if self.one.getPiece() == 'O':
				winner = self.one
				over = True
			else:
				winner = self.two
				over = True
		self.over = over
		return over



















