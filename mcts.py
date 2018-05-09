import time
import math
import random
from node import treeNode

class mcts():
    def __init__(self, timeLimit=None, iterationLimit=None, explorationConstant=1/math.sqrt(2), rolloutPolicy=randomPolicy):
        if timeLimit != None:
            if iterationLimit != None:
                raise ValueError("Cannot have both a time limit and an iteration limit")
            # time taken for each MCTS search in milliseconds
            self.timeLimit = timeLimit
            self.limitType = 'time'
        else:
            if iterationLimit == None:
                raise ValueError("Must have either a time limit or an iteration limit")
            # number of iterations of the search
            if iterationLimit<1:
                raise ValueError("Iteration limit must be greater than one")
            self.searchLimit = iterationLimit
            self.limitType = 'iterations'
        self.explorationConstant = explorationConstant
        self.rollout = rolloutPolicy

    def search(self, initialState):
        self.root = treeNode(initialState, None)

        if self.limitType=='time':
            timeLimit = time.time() + self.timeLimit / 1000
            while time.time() < timeLimit:
                self.executeRound()
        else:
            for i in range(self.searchLimit):
                self.executeRound()

        bestChild = self.getBestChild(self.root, 0)
        return self.getAction(self.root, bestChild)

    def executeRound(self):
        node = self.selectNode(self.root)
        reward = self.rollout(node.state)
        self.backpropogate(node, reward)

    def selectNode(self, node):
        while not node.isTerminal:
            if node.isFullyExpanded:
                node = self.getBestChild(node, self.explorationConstant)
            else:
                return self.expand(node)
        return node

    def expand(self, node):
        actions = node.state.getPossibleActions()
        for action in actions:
            if action not in node.children:
                newNode = treeNode(node.state.takeAction(action), node)
                node.children[action] = newNode
                if len(actions)==len(node.children):
                    node.isFullyExpanded = True
                return newNode

        raise Exception("Should never reach here")

    def backpropogate(self, node, reward):
        while node!=None:
            node.numVisits+=1
            node.totalReward+=reward
            node = node.parent

    def getBestChild(self, node, explorationValue):
        bestValue = float("-inf")
        for child in node.children.values():
            nodeValue = child.totalReward/child.numVisits + explorationValue*math.sqrt(2*math.log(node.numVisits)/child.numVisits)
            if nodeValue > bestValue:
                bestValue=nodeValue
                bestNode = child
        return bestNode

    def getAction(self, root, bestChild):
        for action, node in root.children:
            if node==bestChild:
                return action

def randomPolicy(state):
    while not state.isTerminal:
        action = random.choice(state.getPossibleActions())
        state = state.takeAction(action)
    return state.reward
