from board import Board
from move_generation import legal_moves
import os
#coordinates 0,0 is the top left which is the black rook in the starting position

def main():
    board = Board()
    print(board)
    print(board.evaluation_points())
    board.grid[0][0] = 0
    print(board)
    print(board.evaluation_points())
if __name__ == "__main__":
    main()
