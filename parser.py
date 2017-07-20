import re, itertools
import numpy as np



### Data-related

db = open("../pgn_databases/test.pgn", "r")

print(db.read(10000).split("\n\n")[1::2])

f_dict = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

### Board-related

def init_board():
    board = np.zeros((8, 8, 6), dtype=np.int8)
    
    # Pawns
    board[1, :, 0] = -1
    board[6, :, 0] = 1
    
    # Non-royalty
    for j in range(3):
        board[0, [j, 7-j], j+1] = -1
        board[7, [j, 7-j], j+1] = 1
    
    # Queens
    board[0, 3, 4] = -1
    board[7, 3, 4] = 1
    
    # Kings
    board[0, 4, 5] = -1
    board[7, 4, 5] = 1
    
    return board

    
def unroll(board):
    return board.ravel()

    
    
### Move-related

def parse_move(move):
    
    # Remove check notation (+)
    pattern = re.compile("\+") 
    move = pattern.sub("", move)    
    
    piece_dict = {"R": 1, "N": 2, "B": 3, "Q": 4, "K": 5}
    ambig = None
    
    # Identify piece type
    if move[0].isupper():
        d = piece_dict[move[0]]
        move = move[1:]
    else:
        d = 0
        if "x" in move:
            ambig = move[0]
            move = move[2:]
    
    # Check for ambiguity in move
    if len(move) == 3:
        ambig = move[0]
        move = move[1:]
    elif len(move) > 3:
        return -1
    
    r, f = 8-int(move[1]), f_dict[move[0]]
    
    return [r, f, d, ambig]

    
    
def find_diags(to):
    """ Finds squares on both diagonals that target square lies on """
    r, f, d, ambig = to
    
    diags = set()
    
    # Down-left    
    r_, f_ = r, f
    while r_ >= 0 and f_ <= 7:
        diags.add((r_, f_))
        r_ -= 1
        f_ += 1
    # Up-right
    r_, f_ = r, f
    while f_ >= 0 and r_ <= 7:
        diags.add((r_, f_))
        r_ += 1
        f_ -= 1    
    # Down-right
    r_, f_ = r, f
    while max(r_, f_) <= 7:
        diags.add((r_, f_))
        r_ += 1
        f_ += 1
    # Up-left
    r_, f_ = r, f
    while min(r_, f_) >= 0:
        diags.add((r_, f_))
        r_ -= 1
        f_ -= 1  
        
    return list(diags)
    
    
    
def move_simple(to, player):
    """
    Wipes old position and adds new position of the single piece in a layer
    """
    r, f, d, ambig = to
    board[:, :, d] = np.multiply(board[:, :, d],
                                 np.array([board[:, :, d] != player]))
    board[r, f, d] = player
    
    
    
def move_KQ(to, player):
    move_simple(to, player=player)
    

    
def move_R(to, player):
    r, f, d, ambig = to
    
    # If there's only one piece of that type
    if np.array([board[:, :, d] == player]).sum() == 1:
        return move_simple(to, player)
    
    # Check to see if it's the only piece of its type on the rank
    elif np.array([board[:, f, d] == player]).sum() == 1:
        board[:, f, d] = np.multiply(board[:, f, d],
                                     np.array([board[:, f, d] != player]))
    
    # Check to see if it's the only piece of its type on the file    
    elif np.array([board[r, :, d] == player]).sum() == 1:
        board[r, :, d] = np.multiply(board[r, :, d],
                                     np.array([board[r, :, d] != player]))
                                     
    # Use the disambiguator            
    else:
        try:
            a = int(ambig)-1
            board[:, a, d] = np.multiply(board[:, a, d],
                                         np.array([board[:, a, d] != player]))
            
        except ValueError:
            a = rank_dict[ambig]
            board[a, :, d] = np.multiply(board[a, :, d],
                                         np.array([board[a, :, d] != player]))
        
    board[r, f, d] = player

    
    
def move_N(to, player):
    r, f, d, ambig = to
    
    # If there's only one piece of that type
    if np.array([board[:, :, d] == player]).sum() == 1:
        return move_simple(to, player)
    
    # Check to see if it's the only one in potential origin squares
    origins = [[2, 1], [2, -1], [1, 2], [1, -2],
               [-1, 2], [-1, -2], [-2, 1], [-2, -1]]
    
    count = 0
    
    for og in origins:
        r_, f_ = np.add([r, f], og)
        if 0 <= r_ <= 7 and 0 <= f_ <= 7:
            if board[r_, f_, d] == player:
                count += 1
                
    if count == 1:
        for og in origins:
            r_, f_ = np.add([r, f], og)
            if 0 <= r_ <= 7 and 0 <= f_ <= 7:
                if board[r_, f_, d] == player:
                    board[r_, f_, d] = 0
                    
    # Use the disambiguator            
    else:
        try:
            a = int(ambig)-1
            board[:, a, d] = np.multiply(board[:, a, d],
                                         np.array([board[:, a, d] != player]))
            
        except ValueError:
            a = rank_dict[ambig]
            board[a, :, d] = np.multiply(board[a, :, d],
                                         np.array([board[a, :, d] != player]))
    
    board[r, f, d] = player
        
    

    
def move_B(to, player):
    r, f, d, ambig = to
   
    # If there's only one piece of that type
    if np.array([board[:, :, d] == player]).sum() == 1:
        return move_simple(to, player)
    
    # Only one bishop on each square colour; so just wipe both diagonals        
    else:
        diags = find_diags(to)
        for square in diags:
            r_, f_ = square
            if board[r_, f_, 3] == player:
                board[r_, f_, 3] = 0
        
    board[r, f, d] = player
    
    
    
def move_P(to, player):
    r, f, d, ambig = to
    
    if ambig is not None:
        a = f_dict[ambig]
        board[r+player, a, d] = 0

    elif board[r+player, f, d] == player:
        board[r+player, f, d] = 0
        
    else:
        board[r+2*player, f, d] = 0
        
    board[r, f, d] = player
    
    
    
    
    
    
    
    