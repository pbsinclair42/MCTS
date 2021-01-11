from __future__ import division

from copy import deepcopy
from mcts import mcts
import random

class KInARow:

    playerNames = {1:'O', -1:'X'}

    def __init__(self, kConnections=4, mColumns=7, nRows=6):
        self.kConnections = kConnections
        self.mColumns = mColumns
        self.nRows = nRows
        self.board = [ [0 for _ in range(self.mColumns)] for _ in range(self.nRows)]
        self.currentPlayer = max(KInARow.playerNames.keys())
        self.isTerminated = None
        self.reward = None
        self.possibleActions = None
        self.winMove = None

    def show(self):
        for row in reversed(self.board):
            rowText = ""
            for x in row:
                if x in self.playerNames:
                    rowText += f" {self.playerNames[x]} "
                else:
                    rowText += " . "
            print(rowText)

    def getCurrentPlayer(self):
        return self.currentPlayer

    def getPossibleActions(self):
        if self.possibleActions is None:
            self.possibleActions = []
            for columnIndex in range(self.mColumns):
                for rowIndex in range(self.nRows):
                    if self.board[rowIndex][columnIndex] == 0:
                        self.possibleActions.append(Action(player=self.currentPlayer,
                                                           rowIndex=rowIndex,
                                                           columnIndex=columnIndex))
                        break
        return self.possibleActions

    def takeAction(self, action):
        newState = deepcopy(self)
        newState.board[action.rowIndex][action.columnIndex] = action.player
        newState.currentPlayer = self.currentPlayer * -1
        newState.isTerminated = None
        newState.possibleActions = None
        newState.winMove = None
        return newState

    def isTerminal(self):

        if self.isTerminated is None:

            self.isTerminated = False
            for rowIndex in range(self.nRows):
                line = self.board[rowIndex]
                lineReward = self.getLineReward(line)
                if lineReward != 0:
                    self.isTerminated = True
                    self.reward = lineReward
                    self.winMove = "k-in-row"
                    break

            if not self.isTerminated:
                for columnIndex in range(self.mColumns):
                    line = []
                    for rowIndex in range(self.nRows):
                        line.append(self.board[rowIndex][columnIndex])
                    lineReward = self.getLineReward(line)
                    if lineReward != 0:
                        self.isTerminated = True
                        self.reward = lineReward
                        self.winMove = "k-in-column"
                        break

            if not self.isTerminated:
                # diagonal: rowIndex = columnIndex + parameter
                for parameter in range(1 - self.mColumns, self.nRows):
                    line = []
                    for columnIndex in range(self.mColumns):
                        rowIndex = columnIndex + parameter
                        if 0 <= rowIndex < self.nRows:
                            line.append(self.board[rowIndex][columnIndex])
                    lineReward = self.getLineReward(line)
                    if lineReward != 0:
                        self.isTerminated = True
                        self.reward = lineReward
                        self.winMove = "k-in-diagonal"
                        break

            if not self.isTerminated:
                # antidiagonal: rowIndex = - columnIndex + parameter
                for parameter in range(0, self.mColumns + self.nRows):
                    line = []
                    for columnIndex in range(self.mColumns):
                        rowIndex = -columnIndex + parameter
                        if 0 <= rowIndex < self.nRows:
                            line.append(self.board[rowIndex][columnIndex])
                    lineReward = self.getLineReward(line)
                    if lineReward != 0:
                        self.isTerminated = True
                        self.reward = lineReward
                        self.winMove = "k-in-antidiagonal"
                        break

            if not self.isTerminated and len(self.getPossibleActions()) == 0:
                self.isTerminated = True
                self.reward = 0

        return self.isTerminated

    def getReward(self):
        assert self.isTerminal()
        assert self.reward is not None
        return self.reward

    def getLineReward(self, line):
        lineReward = 0
        if len(line) >= self.kConnections:
            for player in KInARow.playerNames.keys():
                playerLine = [x == player for x in line]
                playerConnections = 0
                for x in playerLine:
                    if x:
                        playerConnections += 1
                        if playerConnections == self.kConnections:
                            lineReward = player
                            break
                    else:
                        playerConnections = 0
                if lineReward != 0:
                    break
        return lineReward


class Action():
    def __init__(self, player, rowIndex, columnIndex):
        self.player = player
        self.rowIndex = rowIndex
        self.columnIndex = columnIndex

    def __str__(self):
        return str((self.rowIndex, self.columnIndex))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.__class__ == (other.__class__ and
                                  self.player == other.player and
                                  self.rowIndex == other.rowIndex and
                                  self.columnIndex == other.columnIndex)

    def __hash__(self):
        return hash((self.rowIndex, self.columnIndex, self.player))


def main():
    """Example of a KInARow game play between MCTS and random searchers.

    The kConnections and mColumns x nRows board are randomly chosen
    in order to exercise the MCTS time ressource.

    One of the two player is randomly assigned to the MCTS searcher
    for purpose of correctness checking.

    A basic statistics is provided at each MCTS turn."""

    searchers = {}
    searchers["mcts-100i"] = mcts(iterationLimit=200)
    searchers["mcts-50i"] = mcts(iterationLimit=100)

    playerNames = KInARow.playerNames

    playerSearcherNames = {}
    for player in sorted(playerNames.keys()):
         playerSearcherNames[player] = random.choice(sorted(searchers.keys()))

    (k, m, n) = random.choice([(4, 7, 6)])
    currentState = KInARow(kConnections=k, mColumns=m, nRows=n)

    turn = 0
    currentState.show()
    while not currentState.isTerminal():
        turn += 1
        player = currentState.getCurrentPlayer()
        action_count = len(currentState.getPossibleActions())

        searcherName = playerSearcherNames[player]
        searcher = searchers[searcherName]

        action = searcher.search(initialState=currentState)
        statistics = searcher.getStatistics(action)

        currentState = currentState.takeAction(action)

        print(f"at turn {turn} player {playerNames[player]}={player} ({searcherName})" +
              f" takes action {action} amongst {action_count} possibilities")

        print(f"mcts statitics for the chosen action: {statistics['actionTotalReward']} total reward" +
              f" over {statistics['actionNumVisits']} visits")

        print(f"mcts statitics for all explored actions: {statistics['rootTotalReward']} total reward" +
              f" over {statistics['rootNumVisits']} visits")

        print('-'*90)
        currentState.show()

    print('-'*90)
    if currentState.getReward() == 0:
        print(f"game k={k} mxn={m}x{n} terminates; nobody wins")
    else:
        print(f"game k={k} mxn={m}x{n} terminates;" +
              f" player {playerNames[player]}={player} ({searcherName}) wins" +
              f" by {currentState.winMove}")


if __name__ == "__main__":
    main()

