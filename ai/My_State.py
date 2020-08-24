import numpy as np
from goboard import BoardInfo, Player

#game state 
class GameState:
    def __init__(self, board, color):
        #get_board() is a function I wrote in board.
        black_board = board.dense[0,:,:]
        white_board = board.dense[1,:,:]
        black_board = black_board * 2
        self.board = black_board + white_board
        #self.board = board.get_board()
        self.lenth = board.size_x
        if(color == "black"):
            self.color = False
        elif(color == "white"):
            self.color = True
    
    #feild evaluate, 3->out of bounds
    def get_field(self, x, y, direction):
        get_string = np.array([])
        padded_board = np.pad(self.board,((4,4),(4,4)),'constant', constant_values=(3,3))
        pos, diag1, diag2, diag3, diag4 = np.array([x+4,y+4]), np.array([1,1]), np.array([1,-1]), np.array([1,0]), np.array([0,1])
        if(direction == 0): #左下到右上
            pos = pos - 4*diag1
            diag = diag1
        if(direction == 1): #左上到右下
            pos = pos - 4*diag2
            diag = diag2
        if(direction == 2): #左到右
            pos = pos - 4*diag3
            diag = diag3
        if(direction == 3): #上到下
            pos = pos - 4*diag4
            diag = diag4
        for i in range (0,9):
            get_string = np.append(get_string,padded_board[int(pos[0]),int(pos[1])])
            pos = pos + diag
        return get_string  

    #returns the current color of player. every time do/undo move, player changes
    def get_current_player(self):
        if(self.color == True): 
            return "white"
        elif(self.color == False): 
            return "black"

    #get a numpy array shape [13,13]
    def get_state(self):
        return self.board
    
    def do_move(self, color, x, y):
        if(self.board[x,y] == 0):
            if(color == "black"): 
                self.board[x,y] = 2
            elif(color == "white"):
                self.board[x,y] = 1
            else:
                print("!!! Invalid do_move color")
            #self.color = not self.color
        else:
            print("!!! Invalid do_move x,y")
    def change_player(self):
        self.color = not self.color
    
    def undo_move(self, x, y):
        if(self.board[x,y] != 0):
            self.board[x,y] = 0
            self.color = not self.color
        else:
            print("!!! Invalid undo_move")

    def is_empty(self, x, y):
        if(self.board[x,y] == 0):
            return 1
        return 0
    
    #return board lenth
    def get_lenth(self):
        return self.lenth

                
        






