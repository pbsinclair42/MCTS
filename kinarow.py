from __future__ import division

from copy import deepcopy
from mcts import mcts
import random


class KInARowState:

    playerNames = {1:'O', -1:'X'}

    def __init__(self, mColumns=7, nRows=6, kConnections=4):
        self.mColumns = mColumns
        self.nRows = nRows
        self.kConnections = kConnections
        self.board = [ [0 for _ in range(self.mColumns)] for _ in range(self.nRows)]
        self.currentPlayer = max(KInARowState.playerNames.keys())
        self.isTerminated = None
        self.reward = None
        self.possibleActions = None
        self.winingPattern = None

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
                                                           columnIndex=columnIndex,
                                                           rowIndex=rowIndex))
                        break
        return self.possibleActions

    def takeAction(self, action):
        newState = deepcopy(self)
        newState.board[action.rowIndex][action.columnIndex] = action.player
        newState.currentPlayer = self.currentPlayer * -1
        newState.isTerminated = None
        newState.possibleActions = None
        newState.winingPattern = None
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
                    self.winingPattern = "k-in-row"
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
                        self.winingPattern = "k-in-column"
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
                        self.winingPattern = "k-in-diagonal"
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
                        self.winingPattern = "k-in-antidiagonal"
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
            for player in KInARowState.playerNames.keys():
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
    def __init__(self, player, columnIndex, rowIndex):
        self.player = player
        self.rowIndex = rowIndex
        self.columnIndex = columnIndex

    def __str__(self):
        return str((self.columnIndex, self.rowIndex))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.__class__ == (other.__class__ and
                                  self.player == other.player and
                                  self.columnIndex == other.columnIndex and
                                  self.rowIndex == other.rowIndex)

    def __hash__(self):
        return hash((self.columnIndex, self.rowIndex, self.player))


def extractStatistics(searcher, action=None):
    statistics = {}
    statistics['rootNumVisits'] = searcher.root.numVisits
    statistics['rootTotalReward'] = searcher.root.totalReward
    if action is not None:
        statistics['actionNumVisits'] = searcher.root.children[action].numVisits
        statistics['actionTotalReward'] = searcher.root.children[action].totalReward
    return statistics


def main():
    """Example of a "k-in-a-row" game with gravity like "Connect Four".

    The match occurs between two MCTS searchers.

    The kConnections and (mColumns, nRows) board are randomly chosen
    in order to exercise the MCTS time ressource.

    Basic MCTS statistics is provided."""

    searchers = {}
    searchers["mcts-1500ms"] = mcts(timeLimit=1_500)
    searchers["mcts-1000ms"] = mcts(timeLimit=1_000)
    searchers["mcts-500ms"] = mcts(timeLimit=500)
    searchers["mcts-250ms"] = mcts(timeLimit=250)

    playerNames = KInARowState.playerNames

    playerSearcherNames = {}
    for player in sorted(playerNames.keys()):
         playerSearcherNames[player] = random.choice(sorted(searchers.keys()))

    (m, n, k) = random.choice([(7, 6, 4), (8, 7, 5), (9, 8, 6)])
    currentState = KInARowState(mColumns=m, nRows=n, kConnections=k)
    turn = 0
    currentState.show()
    while not currentState.isTerminal():
        turn += 1
        player = currentState.getCurrentPlayer()
        action_count = len(currentState.getPossibleActions())

        searcherName = playerSearcherNames[player]
        searcher = searchers[searcherName]

        action = searcher.search(initialState=currentState)
        statistics = extractStatistics(searcher, action)

        currentState = currentState.takeAction(action)

        print(f"at turn {turn} player {playerNames[player]}={player} ({searcherName})" +
              f" takes action (column, row)={action} amongst {action_count} possibilities")

        print(f"mcts statitics for the chosen action: {statistics['actionTotalReward']} total reward" +
              f" over {statistics['actionNumVisits']} visits")

        print(f"mcts statitics for all explored actions: {statistics['rootTotalReward']} total reward" +
              f" over {statistics['rootNumVisits']} visits")

        print('-'*90)
        currentState.show()

    print('-'*90)
    if currentState.getReward() == 0:
        print(f"game mxn={m}x{n} k={k} terminates; nobody wins")
    else:
        print(f"game mxn={m}x{n} k={k} terminates;" +
              f" player {playerNames[player]}={player} ({searcherName}) wins" +
              f" with pattern {currentState.winingPattern}")


if __name__ == "__main__":
    main()
