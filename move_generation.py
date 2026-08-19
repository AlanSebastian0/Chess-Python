from board import Board

#possible movments that each piece is able to do
knight_moves = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
rook_offsets = [(0,1),(0,-1),(1,0),(-1,0)]
bishop_offsets = [(1,1),(1,-1),(-1,-1),(-1,1)]
king_offsets = rook_offsets + bishop_offsets
queen_offsets = rook_offsets + bishop_offsets

def pseudo_legal_moves(board: Board) -> list: #pseudo legal check filtering has not been added yet
    moves = [] #store a list of tuples of the piece starting square and its ending sqaure
    for row in range(8):
        for col in range(8):
            start_pos = (row,col) #store the starting position of the piece
            piece = board.get_piece((row,col)) #find the piece type
            if piece == 0: #skip move generation logic if square is empty
                continue
            if board.is_own_piece(piece):
                piece_type = abs(piece)
                
                if piece_type == 1:
                    if piece > 0: #white pawn
                        square_ahead = (row-1,col) #coordinates for the square infront of the pawn
                        if board.in_bounds(square_ahead) and board.get_piece(square_ahead) == 0: #check if square is vacant
                            if row - 1 == 0: #pawn promotion logic
                                for promo in [5, 4, 3, 2]: #queen, rook, bishop, knight
                                    moves.append((start_pos, square_ahead, promo))
                            else:
                                moves.append((start_pos, square_ahead))
                                square_ahead = (row-2, col)
                                if row == 6 and board.get_piece(square_ahead) == 0: #double square checking, nested if here for ease
                                    moves.append((start_pos, square_ahead))
                                    
                        for d_col in [1,-1]: #diagonal logic
                            diagonal_square = (row-1, col+d_col)
                            if board.in_bounds(diagonal_square):
                                destination_piece = board.get_piece(diagonal_square) #store the 'piece' if it is in bounds
                                if destination_piece != 0 and not board.is_own_piece(destination_piece): #if not empty and is not the same colour
                                    if row - 1 == 0: #pawn promotion on capture
                                        for promo in [5, 4, 3, 2]:
                                            moves.append((start_pos, diagonal_square, promo))
                                    else:
                                        moves.append((start_pos, diagonal_square))
                                elif diagonal_square == board.en_passant_sq: #en passant capture logic
                                    moves.append((start_pos, diagonal_square))
                    
                    else: #black pawn
                        square_ahead = (row+1, col)
                        if board.in_bounds(square_ahead) and board.get_piece(square_ahead) == 0: #logic for vacant square
                            if row + 1 == 7: #pawn promotion logic
                                for promo in [-5, -4, -3, -2]: #queen, rook, bishop, knight (negative for black)
                                    moves.append((start_pos, square_ahead, promo))
                            else:
                                moves.append((start_pos, square_ahead))
                                square_ahead = (row+2, col)
                                if row == 1 and board.get_piece(square_ahead) == 0:
                                    moves.append((start_pos, square_ahead))
                                    
                        for d_col in [1,-1]:
                            diagonal_square = (row+1,col+d_col)
                            if board.in_bounds(diagonal_square):
                                destination_piece = board.get_piece(diagonal_square)
                                if destination_piece != 0 and not board.is_own_piece(destination_piece):
                                    if row + 1 == 7: #pawn promotion on capture
                                        for promo in [-5, -4, -3, -2]:
                                            moves.append((start_pos, diagonal_square, promo))
                                    else:
                                        moves.append((start_pos, diagonal_square))
                                elif diagonal_square == board.en_passant_sq: #en passant capture logic
                                    moves.append((start_pos, diagonal_square))

                elif piece_type == 2: #knight logic
                    n_moves = generate_singular_moves(board, start_pos, knight_moves)
                    moves += n_moves

                elif piece_type == 3: #bishop
                    bishop_moves = generate_sliding_legal_moves(board,start_pos, bishop_offsets)
                    moves += bishop_moves

                elif piece_type == 4: #rook
                    rook_moves = generate_sliding_legal_moves(board,start_pos, rook_offsets)
                    moves += rook_moves

                elif piece_type == 5: #queen logic
                    queen_moves = generate_sliding_legal_moves(board, start_pos, queen_offsets)
                    moves += queen_moves

                elif piece_type == 6: #king
                    king_moves = generate_singular_moves(board, start_pos,king_offsets)
                    moves += king_moves
                    
                    #castling logic checks if rights exist and squares between king and rook are empty
                    if piece > 0: #white castling
                        if board.castling_rights["white_kingside"] and board.get_piece((7,5)) == 0 and board.get_piece((7,6)) == 0:
                            #checks if the two squares are empy
                            moves.append((start_pos, (7,6))) #checks 
                        if board.castling_rights["white_queenside"] and board.get_piece((7,1)) == 0 and board.get_piece((7,2)) == 0 and board.get_piece((7,3)) == 0:
                            #checks if the three squares are empty for the queen side castle
                            moves.append((start_pos, (7,2)))
                    else: #black castling
                        if board.castling_rights["black_kingside"] and board.get_piece((0,5)) == 0 and board.get_piece((0,6)) == 0:
                            moves.append((start_pos, (0,6)))
                        if board.castling_rights["black_queenside"] and board.get_piece((0,1)) == 0 and board.get_piece((0,2)) == 0 and board.get_piece((0,3)) == 0:
                            moves.append((start_pos, (0,2)))

    return moves

def generate_sliding_legal_moves(board: Board,start_pos: tuple, offset: list) -> list:
    #what to achieve apply offsets until object is hit
    moves = []
    row, col = start_pos
    for d_row, d_col in offset:
        e_row = row + d_row
        e_col = col + d_col
        while board.in_bounds((e_row, e_col)): #while the offset is within the chess board
            end_pos = (e_row, e_col) #end position
            destination_piece = board.get_piece(end_pos)
            if destination_piece != 0:
                if not board.is_own_piece(destination_piece): #checking if ocuupied square is the same as colour as the original piece
                    moves.append((start_pos, end_pos)) #if opposite colour that piece can be captured
                    break
                break #that particular offset has been exhausted its 'sliding' so exit the while loop and go for the next 'ofset'
            moves.append((start_pos, end_pos)) #empty square that can be filled
            e_row += d_row
            e_col += d_col
    return moves

def generate_singular_moves(board: Board, start_pos: tuple, offset: list) -> list:
    moves = []
    row, col = start_pos #get the pieces row and column
    for d_row, d_col in offset:
        #apply the offsets
        e_row = row + d_row
        e_col = col + d_col
        end_pos = (e_row, e_col) #store the end coordinates
        if board.in_bounds(end_pos): #continue if it is within bounds
            destination_piece = board.get_piece(end_pos)
            if destination_piece != 0:
                if not board.is_own_piece(destination_piece):
                    moves.append((start_pos, end_pos)) #if end coordinates is not empty but the occupied square is held by the opposite square it can be captured
                continue
            moves.append((start_pos, end_pos)) #append move if it was empty
            continue
    return moves
def legal_moves(board: Board) -> list:
    moves = []
    pseudo_moves = pseudo_legal_moves(board)
    for move in pseudo_moves:
        board.make_move(*move) #the asterisk unpacks the tuple into 2 or 3 arguments dynamically (passes in automatically)
        if board.is_check(): #check if the pseudo move was illegal
            board.unmake_move()
            continue
        board.unmake_move()
        moves.append(move) #append the moves if it is legal
    return moves
