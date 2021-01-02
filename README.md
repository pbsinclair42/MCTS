# MCTS

This package provides a simple way of using Monte Carlo Tree Search in any perfect information domain.

## Installation

With pip: `pip install mcts`

Without pip: Download the zip/tar.gz file of the [latest release](https://github.com/pbsinclair42/MCTS/releases), extract it, and run `python setup.py install`

## Quick Usage

In order to run MCTS, you must implement a `State` class which can fully describe the state of the world.  It must also implement the following methods:

- `getCurrentPlayer()`: Returns 1 if it is the maximizer player's turn to choose an action, or -1 for the minimizer player
- `getPossibleActions()`: Returns an iterable of all actions which can be taken from this state
- `takeAction(action)`: Returns the state which results from taking action `action`
- `isTerminal()`: Returns whether this state is a terminal state
- `getReward()`: Returns the reward for this state: 0 for a draw, positive for a win by maximizer player or negative for a win by the minimizer player.  Only needed for terminal states.

You must also choose a hashable representation for an action as used in `getPossibleActions` and `takeAction`.  Typically this would be a class with a custom `__hash__` method, but it could also simply be a tuple or a string.

Once these have been implemented, running MCTS is as simple as initializing your starting state, then running:

```python
from mcts import mcts

currentState = MyState()
...
searcher = mcts(timeLimit=1000)
bestAction = searcher.search(initialState=currentState)
currentState = currentState.takeAction(action)
...

```
See [naughtsandcrosses.py](https://github.com/pbsinclair42/MCTS/blob/master/naughtsandcrosses.py) for a simple example.

## Detailed usage
A few customizations are possible through the `mcts` constructor:

- The number of MCTS search rounds can be limited by either a given time limit or a given iteration number. 
- The exploration constant $c$, which appears in the UCT score $w_i/n_i + c\sqrt{{ln N_i}/n_i}$ with theoretical default setting $c=\sqrt 2$, can be adapted to your game.
- The default uniform random rollout/playout policy can be changed.

A few statistics can be retrieved after each MCTS search call (see `naughtsandcrosses.py` example)

More of MCTS theory could be found at https://en.wikipedia.org/wiki/Monte_Carlo_tree_search and cited references.

## Collaborating

Feel free to raise a new issue for any new feature or bug you've spotted. Pull requests are also welcomed if you're interested in directly improving the project.
