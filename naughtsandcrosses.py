from __future__ import division

from copy import deepcopy
from mcts import mcts
from functools import reduce
import operator


class NaughtsAndCrossesState():
    def __init__(self):
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.currentPlayer = 1

    def getCurrentPlayer(self):
        return self.currentPlayer

    def getPossibleActions(self):
        possibleActions = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    possibleActions.append(Action(player=self.currentPlayer, x=i, y=j))
        return possibleActions

    def takeAction(self, action):
        newState = deepcopy(self)
        newState.board[action.x][action.y] = action.player
        newState.currentPlayer = self.currentPlayer * -1
        return newState

    def isTerminal(self):
        for row in self.board:
            if abs(sum(row)) == 3:
                return True
        for column in list(map(list, zip(*self.board))):
            if abs(sum(column)) == 3:
                return True
        for diagonal in [[self.board[i][i] for i in range(len(self.board))],
                         [self.board[i][len(self.board) - i - 1] for i in range(len(self.board))]]:
            if abs(sum(diagonal)) == 3:
                return True
        return reduce(operator.mul, sum(self.board, []), 1)

    def getReward(self):
        for row in self.board:
            if abs(sum(row)) == 3:
                return sum(row) / 3
        for column in list(map(list, zip(*self.board))):
            if abs(sum(column)) == 3:
                return sum(column) / 3
        for diagonal in [[self.board[i][i] for i in range(len(self.board))],
                         [self.board[i][len(self.board) - i - 1] for i in range(len(self.board))]]:
            if abs(sum(diagonal)) == 3:
                return sum(diagonal) / 3
        return False


class Action():
    def __init__(self, player, x, y):
        self.player = player
        self.x = x
        self.y = y

    def __str__(self):
        return str((self.x, self.y))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.x == other.x and self.y == other.y and self.player == other.player

    def __hash__(self):
        return hash((self.x, self.y, self.player))

def test_01():
    initialState = NaughtsAndCrossesState()
    # 1 first 1 step win
    # deep=1,2: {(0, 1): False, (0, 2): 1.0, (1, 2): False, (2, 1): False, (2, 2): False}
    # deep>=3 : {(0, 1): 1.0, (0, 2): 1.0, (1, 2): False, (2, 1): 1.0, (2, 2): 1.0}
    initialState.board = [[-1, 0, 0], [-1, 1, 0], [1, 0, 0]]
    initialState.currentPlayer = 1

    # 1 first 3 step win
    # deep>=3 : {(0, 0): False, (0, 1): False, (1, 2): False, (2, 1): 1.0, (2, 2): 1.0}
    # deep=2  : {(0, 0): False, (0, 1): False, (1, 2): False, (2, 1): False, (2, 2): False}
    #initialState.board = [[0, 0, -1], [-1, 1, 0], [1, 0, 0]]
    #initialState.currentPlayer = 1

    from mcts import abpruning
    searcher=abpruning(deep=3,safemargin=0.1,gameinf=65535)
    action=searcher.search(initialState,needDetails=True)
    print(searcher.children)
    print(searcher.counter)

if __name__=="__main__":
    #initialState = NaughtsAndCrossesState()
    #searcher = mcts(timeLimit=1000)
    #action = searcher.search(initialState=initialState)
    #print(action)
    test_01()