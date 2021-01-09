# MCTS

This package provides a simple way of using Monte Carlo Tree Search in any perfect information domain.

## Installation

With pip: `pip install mcts`

Without pip: Download the zip/tar.gz file of the [latest release](https://github.com/pbsinclair42/MCTS/releases), extract it, and run `python setup.py install`

## Quick Usage

In order to run MCTS, you must implement a `State` class which can fully describe the state of the world.  It must also implement four methods:

- `getCurrentPlayer()`: Returns 1 if it is the maximizer player's turn to choose an action, or -1 for the minimiser player
- `getPossibleActions()`: Returns an iterable of all `action`s which can be taken from this state
- `takeAction(action)`: Returns the state which results from taking action `action`
- `isTerminal()`: Returns `True` if this state is a terminal state
- `getReward()`: Returns the reward for this state.  Only needed for terminal states.

You must also choose a hashable representation for an action as used in `getPossibleActions` and `takeAction`.  Typically this would be a class with a custom `__hash__` method, but it could also simply be a tuple or a string.

Once these have been implemented, running MCTS is as simple as initializing your starting state, then running:

```python
from mcts import mcts

searcher = mcts(timeLimit=1000)
bestAction = searcher.search(initialState=initialState)
```
Here the unit of `timeLimit=1000` is millisecond. You can also use `iterationLimit=1600` to specify the number of rollouts. Exactly one of `timeLimit` and `iterationLimit` should be specified. The expected reward of best action can be got by setting `needDetails` to `True` in `searcher`.

```python
resultDict = searcher.search(initialState=initialState, needDetails=True)
print(resultDict.keys()) #currently includes dict_keys(['action', 'expectedReward'])
```

See [naughtsandcrosses.py](https://github.com/pbsinclair42/MCTS/blob/master/naughtsandcrosses.py) for a simple example.

## Slow Usage
//TODO

## Collaborating

Feel free to raise a new issue for any new feature or bug you've spotted. Pull requests are also welcomed if you're interested in directly improving the project.
