from player import Player
from game import Game

one = Player('X')
two = Player('O')
TTT = Game(one, two)

TTT.printBoard()

TTT.place(one, 1)
TTT.printBoard()
TTT.place(two, 4)
TTT.printBoard()
TTT.place(one, 2)
TTT.printBoard()
TTT.place(two, 5)
TTT.printBoard()
TTT.place(one, 3)
TTT.printBoard()

print(TTT.isOver())
