from __future__ import division

from copy import deepcopy
from mcts import mcts
from functools import reduce
import operator
import random


class NaughtsAndCrossesState():

    playerNames = {1:'O', -1:'X'}

    def __init__(self, gridSize=3):
        self.gridSize = gridSize
        self.board = [ [0 for _ in range(self.gridSize)] for _ in range(self.gridSize)]
        self.currentPlayer = 1
        self.possibleActions = None

    def show(self):
        for row in self.board:
            row_text = ""
            for cell in row:
                if cell in self.playerNames:
                    row_text += f" {self.playerNames[cell]} "
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
            if abs(sum(row)) == self.gridSize:
                return True
        for column in list(map(list, zip(*self.board))):
            if abs(sum(column)) == self.gridSize:
                return True
        for diagonal in [[self.board[i][i] for i in range(len(self.board))],
                         [self.board[i][len(self.board) - i - 1] for i in range(len(self.board))]]:
            if abs(sum(diagonal)) == self.gridSize:
                return True
        return reduce(operator.mul, sum(self.board, []), 1)

    def getReward(self):
        for row in self.board:
            if abs(sum(row)) == self.gridSize:
                return sum(row) / self.gridSize
        for column in list(map(list, zip(*self.board))):
            if abs(sum(column)) == self.gridSize:
                return sum(column) / self.gridSize
        for diagonal in [[self.board[i][i] for i in range(len(self.board))],
                         [self.board[i][len(self.board) - i - 1] for i in range(len(self.board))]]:
            if abs(sum(diagonal)) == self.gridSize:
                return sum(diagonal) / self.gridSize
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


def main():
    """Example of a NaughtsAndCrossesState game play between MCTS and random searchers.
    The standard 3x3 grid is randomly extended up to 10x10 in order to exercise the MCTS time ressource.
    One of the two player is randomly assigned to the MCTS searcher for purpose of correctness checking.
    A basic statistics is provided at each MCTS turn."""

    playerNames = NaughtsAndCrossesState.playerNames
    mctsPlayer = random.choice(sorted(playerNames.keys()))
    gridSize = random.choice(list(range(3,11)))

    currentState = NaughtsAndCrossesState(gridSize)
    turn = 0
    currentState.show()
    while not currentState.isTerminal():
        turn += 1
        player = currentState.getCurrentPlayer()
        action_count = len(currentState.getPossibleActions())

        if player == mctsPlayer:
            searcher = mcts(timeLimit=1_000)
            searcherName = "mcts-1-second"
            action = searcher.search(initialState=currentState)
            statistics = searcher.getStatistics(action)
        else:
            searcherName = "random"
            action = random.choice(currentState.getPossibleActions())
            statistics = None

        currentState = currentState.takeAction(action)
        print(f"at turn {turn} player {playerNames[player]}={player} ({searcherName}) takes action {action} amongst {action_count} possibilities")

        if statistics is not None:
            print(f"mcts statitics for the chosen action: {statistics['actionTotalReward']} total reward over {statistics['actionNumVisits']} visits")
            print(f"mcts statitics for all explored actions: {statistics['rootTotalReward']} total reward over {statistics['rootNumVisits']} visits")

        print('-'*90)
        currentState.show()

    print('-'*90)
    if currentState.getReward() == 0:
        print(f"game {gridSize}x{gridSize} terminates; nobody wins")
    else:
        print(f"game {gridSize}x{gridSize} terminates; player {playerNames[player]}={player} ({searcherName}) wins")


if __name__ == "__main__":
    main()

