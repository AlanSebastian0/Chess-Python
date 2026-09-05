dangerous_offsets = [
            (0, 1), (0, -1), (1, 0), (-1, 0),    # Straight (indices 0-3)
            (1, 1), (1, -1), (-1, -1), (-1, 1)   # Diagonal (indices 4-7)
        ]
knight_moves = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]

class Board:
    #Rook = -4, knight = -2, Queen = -5, King = -6, bishop = -3 pawn = -1. Negative numbers indicate black and positive are white
    def __init__(self):
        self.grid = self.start_grid()
        self.turn = "White"
        self.en_passant_sq = None
        self.castling_rights = {"white_kingside" : True, "white_queenside" : True, "black_kingside" : True, "black_queenside" : True}
        self.move_count = 0
        self.white_king_location = (7,4)
        self.black_king_location = (0,4)
        self.history = [] #stores history of moves and captured pieces for unmake_move

    def evaluation_points(self):
        eval = 0 #points storage
        for row in range(8):
            for col in range(8):
                pos = (row,col)
                piece = self.get_piece(pos)
                piece_type = abs(piece)
                if piece == 1 or piece == -1: #pawn
                    eval += piece
                elif piece_type == 2 or piece_type == 3: #knight and bishop
                    eval += 3 if piece > 0 else -3
                elif piece_type == 4: #rook
                    eval += 5 if piece > 0 else -5
                elif piece_type == 5:
                    eval += 9 if piece > 0 else -9
        return eval

                    
    def start_grid(self): #initilaises the board in its starting positon
        grid = [[0 for _ in range(8)] for _ in range(8)]
        grid[0] = [-4,-2,-3,-5,-6,-3,-2,-4]
        grid[1] = [-1 for _ in range(8)]
        grid[-1] = [4,2,3,5,6,3,2,4]
        grid[-2] = [1 for _ in range(8)]
        return grid

    def get_piece(self,pos: tuple) -> int: #returns the piece occuping a sqaure
        row,col = pos[0],pos[1]
        return self.grid[row][col]

    def is_empty(self,pos: tuple) -> bool: #checks if a sqaure is empty
        row,col = pos
        result = True if self.grid[row][col] == 0 else False
        return result

    def is_own_piece(self,piece: int) -> bool: #checks if a piece is of the same colour of a players turn
        if (piece > 0 and self.turn == "White"):
            return True
        if (piece < 0 and self.turn == "Black"):
            return True
        return False

    def in_bounds(self,pos: tuple) -> bool: #checks if a position is within boundaries
        row,col = pos
        if row >= 8 or col >= 8 or row < 0 or col < 0:
            return False
        return True

    def make_move(self,start_square: tuple, end_square: tuple, promotion_piece: int = None): #make move does not change the turns, MANUAL self.turn is required promotion piece by defult is set to known if it was not passed in
        piece = self.get_piece(start_square)
        captured_piece = self.get_piece(end_square) #store captured piece before overwriting
        Srow,Scol = start_square
        Erow,Ecol = end_square

        #save current state for unmake_move before they are changed
        old_ep = self.en_passant_sq
        old_rights = self.castling_rights.copy() #must copy dictionary so it doesnt reference the same memory 
        is_en_passant = False
        is_castle = False
        #en passant logic 
        if abs(piece) == 1 and Scol != Ecol and captured_piece == 0: #diagonal move to empty square means en passant
            is_en_passant = True
            captured_piece = self.grid[Srow][Ecol] #the actual piece captured is adjacent to start square
            self.grid[Srow][Ecol] = 0 #remove the captured pawn from the board

        #castling logic
        if abs(piece) == 6 and abs(Scol - Ecol) == 2: #king moving two squares means castling K = 6
            is_castle = True
            #logic is true for both colours
            if Ecol == 6: #kingside castle
                self.grid[Erow][5] = self.grid[Erow][7] #move rook next to king
                self.grid[Erow][7] = 0 #empty original rook square
            elif Ecol == 2: #queenside castle
                self.grid[Erow][3] = self.grid[Erow][0]
                self.grid[Erow][0] = 0

        #update king location trackers
        if piece == 6: self.white_king_location = end_square #update the kings location when it moves to common variable
        if piece == -6: self.black_king_location = end_square

        #move the main piece on the grid
        self.grid[Srow][Scol] = 0

        #promotion logic, this is also handled in move_generation.py
        if promotion_piece is not None:
            self.grid[Erow][Ecol] = promotion_piece
        else:
            self.grid[Erow][Ecol] = piece

        if abs(piece) == 1 and abs(Srow - Erow) == 2: 
        #set en passant square for NEXT move if pawn moved two squares
            self.en_passant_sq = ((Srow + Erow) // 2, Scol) #the square directly behind the jumping pawn
        else:
            self.en_passant_sq = None

        #update castling rights if king or rooks move, or if a rook is captured in its corner
        self.update_castling_rights(start_square, end_square)

        self.history.append((start_square, end_square, piece, captured_piece, old_ep, old_rights, is_en_passant, is_castle)) 
        #store EVERYTHING needed to reverse this move

    def update_castling_rights(self, start_square: tuple, end_square: tuple): #helper function to update castling_rights if a king or rook is moved castling rights are apprioately cancelled
        #white rights
        if start_square == (7,4): #white king moved
            self.castling_rights["white_kingside"] = False
            self.castling_rights["white_queenside"] = False
        if start_square == (7,7) or end_square == (7,7): self.castling_rights["white_kingside"] = False #white kingside rook moved or captured
        if start_square == (7,0) or end_square == (7,0): self.castling_rights["white_queenside"] = False #white queenside rook moved or captured

        #black rights
        if start_square == (0,4): #black king moved
            self.castling_rights["black_kingside"] = False
            self.castling_rights["black_queenside"] = False
        if start_square == (0,7) or end_square == (0,7): self.castling_rights["black_kingside"] = False
        if start_square == (0,0) or end_square == (0,0): self.castling_rights["black_queenside"] = False

    def is_check(self) -> bool:
        # Get king square for current turn
        distance = tuple(x-y for x,y in zip(self.white_king_location, self.black_king_location))
        if abs(distance[0]) <= 1 and abs(distance[1]) <= 1:
            return True #checks if the kings are 'touching' each other
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
                    break #ther enemies block the line of site

                curr_row += d_row #empty square keeping on applying the offsets
                curr_col += d_col
        #Knight offsets
        for d_row, d_col in knight_moves:
            curr_row = k_row + d_row
            curr_col = k_col + d_col
            if self.in_bounds((curr_row, curr_col)):
                piece = self.get_piece((curr_row, curr_col))
                if abs(piece) == 2 and not self.is_own_piece(piece):
                    return True

        pawn_offsets = [(-1,1), (-1,-1)] if self.turn == "White" else [(1,-1), (1,1)]
        for d_row, d_col in pawn_offsets:
            curr_row = k_row + d_row
            curr_col = k_col + d_col
            if self.in_bounds((curr_row, curr_col)):
                piece = self.get_piece((curr_row, curr_col))
                if abs(piece) == 1 and not self.is_own_piece(piece):
                    return True

        return False  #return false when a check was not detected

    def unmake_move(self): #undoes the last made move using history stack
        if not self.history:
            return #nothing to undo

        #pop all 8 variables saved during make_move, also removes them fro storage
        start_square, end_square, moved_piece, captured_piece, old_ep, old_rights, is_en_passant, is_castle = self.history.pop()
        Srow, Scol = start_square
        Erow, Ecol = end_square

        #restore global board states
        self.en_passant_sq = old_ep
        self.castling_rights = old_rights

        #restore kings location to starting square
        if moved_piece == 6: self.white_king_location = start_square 
        if moved_piece == -6: self.black_king_location = start_square
        
        #3. put moved piece back
        self.grid[Srow][Scol] = moved_piece 

        #handle grid restoration based on move type
        if is_en_passant:
            self.grid[Erow][Ecol] = 0 #square pawn moved to is empty again
            self.grid[Srow][Ecol] = captured_piece #put captured pawn back beside the starting square
        else:
            self.grid[Erow][Ecol] = captured_piece #restore captured piece or 0 on the destination square

         #restore rook position if it was a castle
        if is_castle:
            if Ecol == 6: #kingside
                self.grid[Erow][7] = self.grid[Erow][5] #put rook back in corner
                self.grid[Erow][5] = 0 #empty the square next to king
            elif Ecol == 2: #queenside
                self.grid[Erow][0] = self.grid[Erow][3]
                self.grid[Erow][3] = 0

    def __repr__(self):
        output = ""
        for row in self.grid:
            output = output + str(row) + "\n"
        return output

def main():
    pass

if __name__ == "__main__":
    main()
