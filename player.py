class Player(object):

	def __init__(self, piece):
		self.piece = piece
		self.turn = False

	def getPiece(self):
		return self.piece;

	def setPiece(self):
		self.piece = piece