# MCTS

This package provides a simple way of using Monte Carlo Tree Search in any perfect information domain.

## Installation

With pip: `pip install mcts`

Without pip: Download the zip/tar.gz file of the [latest release](https://github.com/pbsinclair42/MCTS/releases), extract it, and run `python setup.py install`

## Quick Usage

In order to run MCTS, you must implement a `State` class which can fully describe the state of the world.  It must also implement the following methods:

- `getCurrentPlayer()`: Returns 1 if it is the maximizer player's turn to choose an action, or -1 for the minimiser player
- `getPossibleActions()`: Returns an iterable of all actions which can be taken from this state
- `takeAction(action)`: Returns the state which results from taking action `action`
- `isTerminal()`: Returns whether this state is a terminal state
- `getReward()`: Returns the reward for this state: 0 for a draw, positive for a win by maximizer player or negative for a win by the minimizer player. Only needed for terminal states.

You must also choose a hashable representation for an action as used in `getPossibleActions` and `takeAction`.  Typically this would be a class with a custom `__hash__` method, but it could also simply be a tuple or a string.

Once these have been implemented, running MCTS is as simple as initializing your starting state, then running:

```python
from mcts import mcts

currentState = MyState()
...
searcher = mcts(timeLimit=1000)
bestAction = searcher.search(initialState=currentState)
...
```
See [naughtsandcrosses.py](./naughtsandcrosses.py) for a simple example.

See [connectmnk.py](./connectmnk.py) for another example that runs a full *Connect(m,n,k,1,1)* game between two MCTS searchers.

When initializing the MCTS searcher, there are a few optional parameters that can be used to optimize the search:

- `timeLimit`: the maximum duration of the search in milliseconds. Exactly one of `timeLimit` and `iterationLimit` must be set.
- `iterationLimit`: the maximum number of search iterations to be carried out. Exactly one of `timeLimit` and `iterationLimit` must be set.
- `explorationConstant`: a weight used when searching to help the algorithm prioritize between exploring unknown areas vs deeper exploring areas it currently believes to be valuable. The higher this constant, the more the algorithm will prioritize exploring unknown areas. Default value is √2.
- `rolloutPolicy`: the policy to be used in the roll-out phase when simulating one full play-out. Default is a random uniform policy



## Detailed Information
//TODO

## Collaborating

Feel free to raise a new issue for any new feature or bug you've spotted. Pull requests are also welcomed if you're interested in directly improving the project.
