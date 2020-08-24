import time
import random
import numpy as np
from goboard import Player, BoardInfo, GuiManager
from .My_State import GameState
from .My_GetMoves import GetMoves
from .My_Evaluate import Evaluate

#超時問題


#Player to play game
class Ai(Player):
    def __init__(self, color, **kwargs):
        super(Ai, self).__init__(color)
        try:
            size_x, size_y = kwargs['board_size']
            self.value = np.zeros((size_x, size_y))
            self.color = color
        except IndexError:
            self.value = np.zeros((13, 13))
    #Negmax algorithm
    def NegMax(self, state, move, depth, alpha, beta):
        best_value = -1000000 #-無限大
        
        if depth == 0 :
            eval_value = Evaluate(state,state.get_current_player()).evaluate_state()
            state.change_player()
            return eval_value
        else:
            all_moves = GetMoves(state, state.get_current_player(), self.depth, self.start).get_all()
            """if(all_moves == state.get_current_player()):    #player wins
                return 10000
            elif(all_moves == state.get_current_player()):    #opponent wins
                return -10000"""
            
            for x in range(np.size(all_moves,0)):
                state.do_move(state.get_current_player(),int(all_moves[x,0]),int(all_moves[x,1]))
                move_value = - self.NegMax(state, all_moves[x,:], depth-1, -beta, -alpha)
                state.undo_move(int(all_moves[x,0]),int(all_moves[x,1]))
                if(move_value > best_value):
                    best_value = move_value
                if(best_value > alpha):
                    alpha = best_value
                if(best_value >= beta): break
        return best_value

    #Return the best x,y for player. ai_ai_gui_demo.py calls this function
    def get_action(self, board: BoardInfo, timeout) -> (int, int):
        self.start = time.time()
        state = GameState(board, self.color)  #self color = "white"
        if(timeout <= 6.0): self.depth = 1  #timeout counts down from 50, and is set to 6 once reaches 6
        else: self.depth = 2
        
        alpha = -1000000 #-無限大
        beta = 1000000 #+無限大
        best_value = -1000000 #-無限大
        all_moves = GetMoves(state, self.color, self.depth, self.start).get_all()
        #if threat/advance, do move
        if(all_moves.shape[0] == 1):
            return int(all_moves[0,0]), int(all_moves[0,1])
        #search for best move
        best_move = all_moves[0,:]
        current_player = state.get_current_player()
        for x in range(np.size(all_moves,0)):
            if(self.depth == 1):
                break
            state.do_move(current_player,int(all_moves[x,0]),int(all_moves[x,1]))
            move_value = self.NegMax(state, all_moves[x,:], self.depth-1, alpha, beta)
            state.undo_move(int(all_moves[x,0]),int(all_moves[x,1]))
            if(move_value > best_value):
                best_value = move_value
                best_move = all_moves[x,:]
            if(best_value > alpha):
                alpha = best_value
            if(best_value >= beta): break
        return int(best_move[0]), int(best_move[1])
