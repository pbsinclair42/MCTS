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

### Alpha-Beta Pruning

The use of alpha-beta pruning is almost the same as MCTS. The only different is that `getReward()` is needed for all states.

```python
from mcts import abpruning
searcher=abpruning(deep=3)
bestAction=searcher.search(initialState)
```

The parameters for `abpruning`'s construction function are

* deep      : search deepth;
* safemargin: normally alpha-beta pruning will break when `beta <= alpha`, safemargin strengthen this to `beta + safemargin <= alpha` for situations where eval function is not very accurate;
* gameinf   : an upper bound of getReward() return values used as "inf" in algorithm.

Details of chlidren can be found in `searcher.children` after `search()` is called. `searcher.children` is a dictinary looks like {action:value}.

## Slow Usage

### Write Your Own Policy

The default policy for this package is `randomPolicy` defined in `mcts.py`. Its structure is

```
def randomPolicy(state):
    while not state.isTerminal():
        action = random.choice(state.getPossibleActions())
        state = state.takeAction(action)
    return state.getReward()
```

By substituting it with a stronger policy, you can make the search more efficient. The new policy should be a function which takes `state` as its input and return reward from the point of view of `state`'s current player and will be hand over to mcts by changing `rolloutPolicy=randomPolicy` in `mcts`'s construct function. Pay attention to the sign of reward the policy function returned. Or it will play for its opponent. For example, suppose I have trained a neural network which can estimate the expected reward even the state is not terminal; I can use it to accelerate the rollout

```
def nnPolicy(state):
    if state.isTerminal():
        return state.getReward()
    else:
        return reward_estimated_by_neural_network
```

### More
//TODO

## Collaborating

Feel free to raise a new issue for any new feature or bug you've spotted. Pull requests are also welcomed if you're interested in directly improving the project.
