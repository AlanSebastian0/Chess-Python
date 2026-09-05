from board import Board
from move_generation import legal_moves,perft
import os
#coordinates 0,0 is the top left which is the black rook in the starting position

def main():
    board = Board()
    for i in range(1,4):
        print(perft(board,depth=i))

if __name__ == "__main__":
    main()
