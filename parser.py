import re
import numpy as np



### Data-related

db = open("../pgn_databases/test.pgn", "r")

print(db.read(10000).split("\n\n")[1::2])



### Board-related

def init_board():
    board = np.zeros((8, 8, 6), dtype=np.int8)
    
    # Pawns
    board[1, :, 0] = -1
    board[6, :, 0] = -1
    
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
    
    # Strip down to just the move
    pattern = re.compile("[\Wx]+") 
    move = pattern.sub("", move)
    
    piece_dict = {"R": 1, "N": 2, "B": 3, "Q": 4, "K": 5}
    
    if move[0].isupper():
        d = piece_dict[move[0]]
        move = move[1:]
    else:
        d = 0
    
    rank_dict = {"a": 7, "b": 6, "c": 5, "d": 4, "e": 3, "f": 2, "g": 1, "h": 0}
    
    r, f = rank_dict[move[0]], int(move[1])-1
    
    return [r, f, d]

    
def move_simple(to, player)
    """
    Wipes old position and adds new position of the single piece in a layer
    """
    r, f, d = to
    board[:, :, d] = np.multiply(board[:, :, d],
                                 np.array([board[:, :, d] != player]))
    board[r, f, d] = player
    
def move_KQ(to, player):
    move_simple(to, player=player)
    

def move_R(to, player):
    r, f, d = to
   
    if ([board[:, :, d] == player].sum() == 1):
        move_simple(to, player)
        
    elif ([board[:, f, d] == player].sum() == 1):
        board[:, f, d] = np.multiply(board[:, f, d],
                                     np.array([board[:, f, d] != player]))
        board[r, f, d] = player
        
    elif ([board[r, :, d] == player].sum() == 1):
        board[r, :, d] = np.multiply(board[r, :, d],
                                     np.array([board[r, :, d] != player]))
        board[r, f, d] = player
                
    else:
        return -1
        
        
    
def move_N(to, player):
    pass
    
    
def move_B(to, player):
    pass
    
    
def move_P(to, player):
    pass