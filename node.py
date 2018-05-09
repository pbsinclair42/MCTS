class treeNode():
    numVisits = 0
    totalReward = 0
    children = {}

    def __init__(self, state, parent):
        self.state = state
        self.isTerminal = state.isTerminal
        self.isFullyExpanded = self.isTerminal
        self.parent = parent


    def __eq__(self, other):
        return self.state == other.state
