import numpy as np
from goboard import BoardInfo, Player
from .My_Evaluate import Evaluate
import time


class GetMoves:
    def __init__(self, state, player, depth, start_time):
        self.state = state
        self.player = player
        self.empty_check = True
        self.depth = depth
        self.start_time = start_time
        if(player == "white"): 
            self.color = 1 
        elif(player == "black"): 
            self.color = 2

    def get_all(self):
        #Check if the board is still empty 
        all_moves = np.empty((0,3)) 
        threatResponses = np.empty((0,3)) # (x,y,priority)
        advanceResponses = np.empty((0,2))
        #score_moves = np.empty((0,3)) 

        for x in range (self.state.get_lenth()):
            for y in range (self.state.get_lenth()):
                #check win (因為沒用到樹所以目前沒有用到)
                """if (self.state.is_empty(x, y) == False):
                    winner = self.checkwin(x,y)
                    if(winner == 1): #white wins
                        return "white"
                    if(winner == 2): #black wins
                        return "black"""
                #判斷有沒有夠時間
                if((time.time()-self.start_time>2) and (self.depth == 1)):
                    print("no time")
                    if(threatResponses.shape[0] != 0):
                        return np.matrix([[threatResponses[0,0],threatResponses[0,1]]])
                    temp = all_moves.view(np.ndarray)
                    all_moves = temp[temp[:,2].argsort()[::-1]]
                    return all_moves[0:1,0:3]
                if (self.state.is_empty(x, y) == True):
                    with_adjacent, threat, advance, score  = self.hasAdjacent(x, y, 2)
                    #check threat
                    if(advance): 
                        return np.append(advanceResponses,np.matrix([[x, y]]),axis=0)
                    elif(threat != 0):
                        threatResponses = np.append(threatResponses,np.matrix([[x, y, threat]]),axis=0)
                    #avoid taking a spot too far away
                    elif(with_adjacent):           
                        all_moves = np.append(all_moves,np.matrix([[x, y, score]]),axis=0)
                        #int score = Evaluator.evaluateField(self,x, y, player)
                        #scoredMoves = np.append(scoredMoves,np.matrix([[x,y,score]]),axis=0)
        #do most potent threat
        if(threatResponses.shape[0] != 0):
            temp = threatResponses.view(np.ndarray)
            threatResponses = temp[temp[:,2].argsort()]
            return np.matrix([[threatResponses[0,0],threatResponses[0,1]]])
        elif(all_moves.shape[0] == 0):
            return np.matrix([[6,6]])
        else:
            temp = all_moves.view(np.ndarray)
            all_moves = temp[temp[:,2].argsort()[::-1]]
            return all_moves[0:3,0:3] #get first 3 high scores, [x,y]


    def checkwin(self, row, col):
        enemy = (3 - self.color)
        for i in range (4):
            get_string = self.state.get_field(row, col, i)
            if((int(get_string[0]) == enemy) & (int(get_string[1]) == enemy) & (int(get_string[2]) == enemy) & (int(get_string[3]) == enemy) & (int(get_string[4]) == enemy) ):
                return enemy
            if((int(get_string[0]) == self.color) & (int(get_string[1]) == self.color) & (int(get_string[2]) == self.color) & (int(get_string[3]) == self.color) & (int(get_string[4]) == self.color) ):
                return self.color
        return 0 #noone wins


    def hasAdjacent(self, row, col, distance):
        enemy = (3 - self.color)
        with_adjacent = False
        threat = 0
        advance = False
        score = 0
        for i in range (4):
            get_string = self.state.get_field(row, col, i)
            adjacent_string = get_string[(4-distance):(5+distance)]

            #advance
            #11110
            if((int(get_string[0]) == self.color) & (int(get_string[1]) == self.color) & (int(get_string[2]) == self.color) & (int(get_string[3]) == self.color) ):
                advance = True
                #print("1110")
                return with_adjacent, threat, advance, score
            if((int(get_string[5]) == self.color) & (int(get_string[6]) == self.color) & (int(get_string[7]) == self.color) & (int(get_string[8]) == self.color) ):
                advance = True
                #print("1110")
                return with_adjacent, threat, advance, score
            #11011
            if((int(get_string[2]) == self.color) & (int(get_string[3]) == self.color) & (int(get_string[5]) == self.color) & (int(get_string[6]) == self.color) ):
                advance = True
                #print("11011")
                return with_adjacent, threat, advance, score
            #10111, 11101
            if((int(get_string[3]) == self.color) & (int(get_string[5]) == self.color) & (int(get_string[6]) == self.color) & (int(get_string[7]) == self.color) ):
                advance = True
                #print("10111")
                return with_adjacent, threat, advance, score
            if((int(get_string[1]) == self.color) & (int(get_string[2]) == self.color) & (int(get_string[3]) == self.color) & (int(get_string[5]) == self.color) ):
                advance = True
                #print("11101")
                return with_adjacent, threat, advance, score
            
            #threat
            #22220
            if((int(get_string[0]) == enemy) & (int(get_string[1]) == enemy) & (int(get_string[2]) == enemy) & (int(get_string[3]) == enemy) ):
                threat = 1
                #print("22220")
                return with_adjacent, threat, advance, score
            if((int(get_string[5]) == enemy) & (int(get_string[6]) == enemy) & (int(get_string[7]) == enemy) & (int(get_string[8]) == enemy) ):
                threat = 1
                #print("02222")
                return with_adjacent, threat, advance, score
            #22022
            if((int(get_string[2]) == enemy) & (int(get_string[3]) == enemy) & (int(get_string[5]) == enemy) & (int(get_string[6]) == enemy)):
                threat = 1
                #print("22022")
                return with_adjacent, threat, advance, score
            #22202
            if((int(get_string[1]) == enemy) & (int(get_string[2]) == enemy) & (int(get_string[3]) == enemy) & (int(get_string[5]) == enemy)):
                threat = 1
                #print("22202")
                return with_adjacent, threat, advance, score
            #20222
            if((int(get_string[3]) == enemy) & (int(get_string[5]) == enemy) & (int(get_string[6]) == enemy) & (int(get_string[7]) == enemy)):
                threat = 1
                #print("20222")
                return with_adjacent, threat, advance, score
            #022020
            if((int(get_string[3]) == enemy) & (int(get_string[5]) == enemy) & (int(get_string[6]) == enemy) & (int(get_string[2]) == 0) & (int(get_string[7]) == 0)):
                threat = 2
                #print("022020")
                return with_adjacent, threat, advance, score
            if((int(get_string[2]) == enemy) & (int(get_string[3]) == enemy) & (int(get_string[5]) == enemy)& (int(get_string[1]) == 0)& (int(get_string[6]) == 0)):
                threat = 2
                #print("020220")
                return with_adjacent, threat, advance, score
            #02220
            if((int(get_string[1]) == enemy) & (int(get_string[2]) == enemy) & (int(get_string[3]) == enemy) & (int(get_string[0]) == 0)):
                threat = 2
                #print("02220")
                return with_adjacent, threat, advance, score
            if((int(get_string[5]) == enemy) & (int(get_string[6]) == enemy) & (int(get_string[7]) == enemy) & (int(get_string[8]) == 0)):
                threat = 2
                #print("02220")
                return with_adjacent, threat, advance, score
                                
            # adjacent_no threats, no advances
            for i in range (0,(2*distance + 1)):
                if(int(adjacent_string[i]) != 0):
                    if(int(adjacent_string[i]) != 3.0):
                        with_adjacent = True
                        break
        #return scored moves(evaluated moves)
        if(with_adjacent):
            self.state.do_move(self.state.get_current_player(),row,col)
            score = Evaluate(self.state,self.state.get_current_player()).evaluate_state()
            self.state.undo_move(row,col)

        return with_adjacent, threat, advance, score
