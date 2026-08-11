from move_generation import generate_legal_moves
dangerous_offsets = [
            (0, 1), (0, -1), (1, 0), (-1, 0),    # Straight (indices 0-3)
            (1, 1), (1, -1), (-1, -1), (-1, 1)   # Diagonal (indices 4-7)
        ]
class Board: #hello star
    #Rook = -4, knight = -2, Queen = -5, King = -6, bishop = -3 pawn = -1. Negative numbers indicate black and positive are white
    def __init__(self):
        self.grid = self.start_grid()
        self.turn = "White"
        self.en_passant_sq = None
        self.castling_rights = {"white_kingside" : True, "white_queenside" : True, "black_kingside" : True, "black_queenside" : True}
        self.move_count = 0
        self.white_king_location = (7,4)
        self.black_king_location = (0,4)
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
        if piece == 6: self.white_king_location = end_square #update the kings location when it moves to common variable
        if piece == -6: self.black_king_location = end_square
        Srow,Scol = start_square
        Erow,Ecol = end_square
        self.grid[Srow][Scol] = 0
        self.grid[Erow][Ecol] = piece
        self.turn = "Black" if self.turn == "White" else "White"

    def make_move(self, start_square: tuple, end_square: tuple):
        piece = self.get_piece(start_square)
        if piece == 6: 
            self.white_king_location = end_square
        if piece == -6: 
            self.black_king_location = end_square
            
        Srow, Scol = start_square
        Erow, Ecol = end_square
        self.grid[Srow][Scol] = 0
        self.grid[Erow][Ecol] = piece
        self.turn = "Black" if self.turn == "White" else "White"

    def is_check(self) -> bool:
        # Get king square for current turn
        king_square = self.white_king_location if self.turn == "White" else self.black_king_location
        k_row, k_col = king_square
        # First 4 offsets are straight (Rooks), last 4 are diagonal (Bishops)
        for index, (d_row, d_col) in enumerate(dangerous_offsets): #sliding logic
            curr_row = k_row + d_row
            curr_col = k_col + d_col

            while self.in_bounds((curr_row, curr_col)): #step forward according to the ray until end board or other
                piece = self.get_piece((curr_row, curr_col))

                if piece != 0: #stop looking if friendly piece is encountered
                    if self.is_own_piece(piece):
                        break
                    piece_type = abs(piece)
                    if piece_type == 5:  # Queen attacks on any ray
                        return True
                    if index < 4 and piece_type == 4:  # Rook on straight ray
                        return True
                    if index >= 4 and piece_type == 3:  # Bishop on diagonal ray
                        return True
                    #other enemy pieces such as pawns, knights and kings block
                    break

                curr_row += d_row #empty square keeping on applying the offsets
                curr_col += d_col
        king_piece = self.get_piece(king_square)
        if king_piece > 0:
            end_pos1 = (k_row-1,k_col+1)
            end_pos2 = (k_row)

        return False  #return false when a check was not detected
    def __repr__(self):
        output = ""
        for row in self.grid:
            output = output + str(row) + "\n"
        return output
def main():
    board = Board()
    moves = generate_legal_moves(board) #right now should generate all of the possible moves of the knights
    print(board)
if __name__ == "__main__":
    main()

