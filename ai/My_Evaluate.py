import numpy as np

"""
* For every five created in one move, the evaluator assigns 50 points, 
* 40 for a five created in 2 moves, 
* 30 for 3 moves, 
* 20 for 4 moves and 
* 10 for 5 moves.
# how many possible fives can be formed and in how many moves.
""" 

#有問題

class Evaluate:
    def __init__(self,state,player):
        self.state = state
        self.player = player
        self.me = 0

    def evaluate_state(self):
        if self.player == "black":
            self.me = 2
            opponent = 1
        if self.player == "white":
            self.me = 1
            opponent = 2
        #evaluate
        score = 0
        spot = self.state.get_state()
        for i in range(0, self.state.get_lenth()):
            for j in range(0, self.state.get_lenth()):
                if spot[i, j] == self.me:
                    score += self.evaluateField(self.state, i, j, self.me)
                elif spot[i, j] == opponent:
                    score -= self.evaluateField(self.state, i, j, opponent)
        return score


    def evaluateField(self, state, row, col, index):
        score = 0
        for dir in range(0, 4):
            score += self.scoreDirection(state.get_field(row, col, dir), index)
        return score

    def scoreDirection(self, array, index):
        score = 0
        val_rule = np.array([50, 40, 30, 20, 10])

        for i in range(0,array.size-4):
            empty = 0
            stones = 0
            for j in range(0,5):
                if int(array[i+j]) == 0:
                    empty+=1
                elif int(array[i+j]) == index:
                    stones+=1
                else:   # Opponent stone in this window, can't form a five
                    break
            if empty == 0 | empty == 5:
                continue
            if stones + empty == 5:
                score +=val_rule[empty]
        return score