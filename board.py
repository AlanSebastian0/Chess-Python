class Board: #hello star
    #Rook = -4, knight = -2, Queen = -5, King = -6, bishop = -3 pawn = -1. Negative numbers indicate black and positive are white
    def __init__(self):
        self.grid = self.start_grid()
        self.turn = "White"
        self.en_passant_sq = None
        self.castling_rights = {"white_kingside" : True, "white_queenside" : True, "black_kingside" : True, "black_queenside" : True}
        self.move_count = 0
    def start_grid(self):
        grid = [[0 for _ in range(8)] for _ in range(8)]
        grid[0] = [-4,-2,-3,-5,-6,-3,-2,-4]
        grid[1] = [-1 for _ in range(8)]
        grid[-1] = [4,2,3,5,6,3,2,4]
        grid[-2] = [1 for _ in range(8)]
        return grid
    def get_piece(self,pos: tuple):
        row,col = pos[0],pos[1]
        return self.grid[row][col]
    def is_empty(self,pos: tuple) -> bool:
        row,col = pos
        result = True if self.grid[row][col] == 0 else False
        return result
    def is_own_piece(self,piece: int) -> bool:
        if (piece > 0 and self.turn == "White"):
            return True
        if (piece < 0 and self.turn == "Black"):
            return True
        return False
    def in_bounds(self,pos: tuple) -> bool:
        row,col = pos
        if row >= 8 or col >= 8 or row < 0 or col < 0:
            return False
        return True
    def make_move(self,start_square: tuple, end_square: tuple):
        piece = self.get_piece(start_square)
        Srow,Scol = start_square
        Erow,Ecol = end_square
        self.grid[Srow][Scol] = 0
        self.grid[Erow][Ecol] = piece
        self.turn = "Black" if self.turn == "White" else "White"


    def __repr__(self):
        output = ""
        for row in self.grid:
            output = output + str(row) + "\n"
        return output
from move_generation import generate_legal_moves
def main():
    board = Board()
    moves = generate_legal_moves(board) #right now should generate all of the possible moves of the knights
    print(board)
if __name__ == "__main__":
    main()

