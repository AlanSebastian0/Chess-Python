from board import Board
from move_generation import generate_legal_moves
import os
#coordinates 0,0 is the top left which is the black rook in the starting position

def main():
    board = Board()
    print(board)
    moves = generate_legal_moves(board)
    total_moves = len(moves)
    print(moves)
    print(f"the total amount of moves is {total_moves}")
if __name__ == "__main__":
    main()
