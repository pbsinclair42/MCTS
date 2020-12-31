from __future__ import division

from copy import deepcopy
from mcts import mcts
from functools import reduce
import operator
import random


class NaughtsAndCrossesState():
    def __init__(self, side=3):
        self.side = side
        self.board = [ [0 for _ in range(side)] for _ in range(side)]
        self.currentPlayer = 1
        self.possibleActions = None

    def show(self):
        for row in self.board:
            row_text = ""
            for cell in row:
                if cell == 1:
                    row_text += " O "
                elif cell == -1:
                    row_text += " X "
                else:
                    row_text += " . "
            print(row_text)

    def getCurrentPlayer(self):
        return self.currentPlayer

    def getPossibleActions(self):
        if self.possibleActions is None:
            self.possibleActions = []
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    if self.board[i][j] == 0:
                        self.possibleActions.append(Action(player=self.currentPlayer, x=i, y=j))
        return self.possibleActions

    def takeAction(self, action):
        newState = deepcopy(self)
        newState.board[action.x][action.y] = action.player
        newState.currentPlayer = self.currentPlayer * -1
        newState.possibleActions = None
        return newState

    def isTerminal(self):
        for row in self.board:
            if abs(sum(row)) == self.side:
                return True
        for column in list(map(list, zip(*self.board))):
            if abs(sum(column)) == self.side:
                return True
        for diagonal in [[self.board[i][i] for i in range(len(self.board))],
                         [self.board[i][len(self.board) - i - 1] for i in range(len(self.board))]]:
            if abs(sum(diagonal)) == self.side:
                return True
        return reduce(operator.mul, sum(self.board, []), 1)

    def getReward(self):
        for row in self.board:
            if abs(sum(row)) == self.side:
                return sum(row) / self.side
        for column in list(map(list, zip(*self.board))):
            if abs(sum(column)) == self.side:
                return sum(column) / self.side
        for diagonal in [[self.board[i][i] for i in range(len(self.board))],
                         [self.board[i][len(self.board) - i - 1] for i in range(len(self.board))]]:
            if abs(sum(diagonal)) == self.side:
                return sum(diagonal) / self.side
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


# Example of a game between two searchers: MCTS versus random
mcts_player = random.choice((1, -1))
player_name = {1:'O', -1:'X'}

game_side = random.choice(list(range(3,11)))
currentState = NaughtsAndCrossesState(side=game_side)
currentState.show()
turn = 0

while not currentState.isTerminal():
    turn += 1
    player = currentState.getCurrentPlayer()

    action_count = len(currentState.getPossibleActions())

    if player == mcts_player:
        searcher = mcts(timeLimit=1_000)
        searcher_name = "mcts-1s"
        action = searcher.search(initialState=currentState)
        totalReward = searcher.getTotalReward()

    else:
        searcher_name = "random"
        action =random.choice(currentState.getPossibleActions())
        totalReward = None

    currentState = currentState.takeAction(action)

    print(f"at turn {turn} player {player_name[player]}={player} ({searcher_name}) takes action {action}" +
          f" amongst {action_count} possibilities")

    if totalReward is not None:
        if totalReward*player > 0:
            print(f"mcts: {totalReward} total reward; winning leaves found !!!")
        else:
            print(f"mcts: {totalReward} total reward; no winning leaf found ...")

    print('-'*90)
    currentState.show()

print('-'*90)
reward = currentState.getReward()

if reward == 0:
    print(f"game {game_side}x{game_side} terminates; nobody wins")
else:
    print(f"game {game_side}x{game_side} terminates; player {player_name[player]}={player} wins")
