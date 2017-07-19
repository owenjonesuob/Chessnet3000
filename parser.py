import re, itertools
import numpy as np



### Data-related

db = open("../pgn_databases/test.pgn", "r")

print(db.read(10000).split("\n\n")[1::2])

rank_dict = {"a": 7, "b": 6, "c": 5, "d": 4, "e": 3, "f": 2, "g": 1, "h": 0}

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
    
    # Remove capture/check notation (x/+)
    pattern = re.compile("[\Wx]+") 
    move = pattern.sub("", move)    
    
    piece_dict = {"R": 1, "N": 2, "B": 3, "Q": 4, "K": 5}
    
    # Identify piece type
    if move[0].isupper():
        d = piece_dict[move[0]]
        move = move[1:]
    else:
        d = 0
        
    # Check for ambiguity in move
    if len(move) == 3:
        ambig = move[0]
        move = move[1:]
    elif len(move) > 3:
        return -1
    else:
        ambig = None
    
    r, f = rank_dict[move[0]], int(move[1])-1
    
    return [r, f, d, ambig]

    
    
def find_diags(to):
    """ Finds squares on both diagonals that target square lies on """
    r, f, d, ambig = to
    
    diags = set()
    
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
        
    return diags
    
    
    
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
   
    if np.array([board[:, :, d] == player]).sum() == 1:
        return move_simple(to, player)
        
    elif np.array([board[:, f, d] == player]).sum() == 1:
        board[:, f, d] = np.multiply(board[:, f, d],
                                     np.array([board[:, f, d] != player]))
        
    elif np.array([board[r, :, d] == player]).sum() == 1:
        board[r, :, d] = np.multiply(board[r, :, d],
                                     np.array([board[r, :, d] != player]))
                
    else:
        try:
            a = int(ambig)-1
            board[:, a, d] = np.multiply(board[:, a, d],
                                         np.array([board[:, a, d] != player]))
            
        except ValueError:
            a = rank_dict(ambig)
            board[a, :, d] = np.multiply(board[a, :, d],
                                         np.array([board[a, :, d] != player]))
        
    board[r, f, d] = player
        
    
def move_N(to, player):
    pass
    
# WIP    
def move_B(to, player):
    r, f, d, ambig = to
   
    if np.array([board[:, :, d] == player]).sum() == 1:
        return move_simple(to, player)
        
    elif np.array(list(range(0, r), f, d] == player]).sum() == 1:
        board[:, f, d] = np.multiply(board[:, f, d],
                                     np.array([board[:, f, d] != player]))
        
    elif np.array([board[r, :, d] == player]).sum() == 1:
        board[r, :, d] = np.multiply(board[r, :, d],
                                     np.array([board[r, :, d] != player]))
                
    else:
        try:
            a = int(ambig)-1
            board[:, a, d] = np.multiply(board[:, a, d],
                                         np.array([board[:, a, d] != player]))
            
        except ValueError:
            rank_dict = {"a": 7, "b": 6, "c": 5, "d": 4, "e": 3, "f": 2, "g": 1, "h": 0}
            a = rank_dict(ambig)
            board[a, :, d] = np.multiply(board[a, :, d],
                                         np.array([board[a, :, d] != player]))
        
    board[r, f, d] = player
    
    
def move_P(to, player):
    pass