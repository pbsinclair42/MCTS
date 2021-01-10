from __future__ import division

from copy import deepcopy
from mcts import mcts
import random

class KInARow:

    playerNames = {1:'O', -1:'X'}

    def __init__(self, k_connections=4, m_columns=7, n_rows=6):
        self.k_connections = k_connections
        self.m_columns = m_columns
        self.n_rows = n_rows
        self.board = [ [0 for _ in range(self.m_columns)] for _ in range(self.n_rows)]
        self.currentPlayer = max(KInARow.playerNames.keys())
        self.isTerminated = None
        self.reward = None
        self.possibleActions = None

    def show(self):
        for row in reversed(self.board):
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
            for column_index in range(self.m_columns):
                for row_index in range(self.n_rows):
                    if self.board[row_index][column_index] == 0:
                        self.possibleActions.append(Action(player=self.currentPlayer,
                                                           row_index=row_index,
                                                           column_index=column_index))
                        break
        return self.possibleActions

    def takeAction(self, action):
        newState = deepcopy(self)
        newState.board[action.row_index][action.column_index] = action.player
        newState.currentPlayer = self.currentPlayer * -1
        newState.isTerminated = None
        newState.possibleActions = None
        return newState

    def isTerminal(self):

        if self.isTerminated is None:

            self.isTerminated = False
            for column_index in range(self.m_columns):
                line = []
                for row_index in range(self.n_rows):
                    line.append(self.board[row_index][column_index])
                    lineReward = self.getLineReward(line)
                    if lineReward != 0:
                        self.isTerminated = True
                        self.reward = lineReward
                        break

            if not self.isTerminated:
                for row_index in range(self.n_rows):
                    line = []
                    for column_index in range(self.m_columns):
                        line.append(self.board[row_index][column_index])
                        lineReward = self.getLineReward(line)
                        if lineReward != 0:
                            self.isTerminated = True
                            self.reward = lineReward
                            break

            ##TODO: add diagonals

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
        if len(line) >= self.k_connections:
            for player in KInARow.playerNames.keys():
                line_player = [True if x == player else False for x in line]
                k = 0
                for x in line_player:
                    if x:
                        k += 1
                        if k == self.k_connections:
                            lineReward = player
                            break
                    else:
                        k = 0
                if lineReward != 0:
                    break
        return lineReward


class Action():
    def __init__(self, player, row_index, column_index):
        self.player = player
        self.row_index = row_index
        self.column_index = column_index

    def __str__(self):
        return str((self.row_index, self.column_index))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.__class__ == (other.__class__ and
                                  self.player == other.player and
                                  self.row_index == other.row_index and
                                  self.column_index == other.column_index)

    def __hash__(self):
        return hash((self.row_index, self.column_index, self.player))


def main():
    """Example of a KInARow game play between MCTS and random searchers.

    The k_connections and m_columns x n_rows board are randomly chosen
    in order to exercise the MCTS time ressource.

    One of the two player is randomly assigned to the MCTS searcher
    for purpose of correctness checking.

    A basic statistics is provided at each MCTS turn."""

    playerNames = KInARow.playerNames
    mctsPlayer = random.choice(sorted(playerNames.keys()))

    (k, m, n) = random.choice([(4, 7, 6)])
    currentState = KInARow(k_connections=k, m_columns=m, n_rows=n)

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
            searcher = mcts(timeLimit=500)
            searcherName = "mcts-0.5-second"
            action = searcher.search(initialState=currentState)
            statistics = searcher.getStatistics(action)
            # searcherName = "random"
            # action = random.choice(currentState.getPossibleActions())
            # statistics = None

        currentState = currentState.takeAction(action)
        print(f"at turn {turn} player {playerNames[player]}={player} ({searcherName})" +
              f" takes action {action} amongst {action_count} possibilities")

        if statistics is not None:
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
        print(f"game k={k} mxn={m}x{n} terminates; player {playerNames[player]}={player} ({searcherName}) wins")


if __name__ == "__main__":
    main()

