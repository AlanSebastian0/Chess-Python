from board import Board

#possible movments that each piece is able to do
knight_moves = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
rook_offsets = [(0,1),(0,-1),(1,0),(-1,0)]
bishop_offsets = [(1,1),(1,-1),(-1,-1),(-1,1)]
king_offsets = rook_offsets + bishop_offsets
queen_offsets = rook_offsets + bishop_offsets
white_pawn_offsets = [(-1,0), (-1,1), (-1,-1)]
black_pawn_offsets = [(1,0), (1,1), (1,-1)]


def generate_legal_moves(board: Board):
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
                    p_moves = []
                    if piece > 0: #checking if pawn is white
                       p_moves =  generate_singular_moves(board,start_pos, white_pawn_offsets) #apply the offset
                       if row == 6: #row 6 is where the starting row of the white pawns are
                           end_pos = (row-2, col) #bounds checking is not required
                           destination_piece = board.get_piece(end_pos)
                           if destination_piece != 0:
                               moves.append((start_pos, end_pos))
                    else:
                        p_moves = generate_singular_moves(board,start_pos, black_pawn_offsets)
                        if row == 1: #row 1 is where the starting row of the black pawns are
                            end_pos = (row+2, col) #bounds checking is not required
                            destination_piece = board.get_piece(end_pos)
                            if destination_piece != 0:
                                moves.append((start_pos, end_pos))
                    moves += p_moves
                elif piece_type == 2: #knight logic
                    n_moves = generate_singular_moves(board, start_pos, knight_moves)
                    moves += n_moves
                elif piece_type == 3: #bishop
                    bishop_moves = generate_sliding_legal_moves(board,start_pos, bishop_offsets)
                    moves += bishop_moves
                elif piece_type == 4: #rook
                    rook_moves = generate_sliding_legal_moves(board,start_pos, rook_offsets)
                    moves += rook_moves
                elif piece_type == 5: #queen
                    queen_moves = generate_sliding_legal_moves(board, start_pos, queen_offsets)
                    moves += queen_moves
                elif piece_type == 6:
                    king_moves = generate_singular_moves(board, start_pos,king_offsets)
                    moves += king_moves
                    
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
