<!-- #region -->
# OCBA-MCTS Performance Evaluation

This repository contains code and resources for reproducing and extending the results from the paper [An Optimal Computing Budget Allocation Tree Policy for Monte Carlo Tree Search](https://arxiv.org/pdf/2009.12407). The focus of the project is to evaluate the performance of different tree policies—specifically UCB (Upper Confidence Bound) and OCBA (Optimal Computing Budget Allocation)—within the Monte Carlo Tree Search (MCTS) framework, applied to a Tic-Tac-Toe game.


## Files in This Repository

The repository is organized into several key files and modules:

- **`tictactoe.py`**:

    - **TicTacToeMove**: A class representing a move in the Tic-Tac-Toe game.
    - **TicTacToeGameState**: A class representing the state of the Tic-Tac-Toe board and the current player.

- **`node.py`**:

    - **StateNode**: A class representing a state node in the MCTS tree.
    - **StateActionNode**: A class representing a state-action node in the MCTS tree.

- **`mcts.py`**:

    - **MonteCarloTreeSearch: The main class implementing the MCTS algorithm. It uses the provided tree policy to guide the search for the optimal move.

- **`tree_policy.py`**:

    - **TreePolicy_UCB**: A class implementing the UCB tree policy for MCTS.
    - **TreePolicy_OCBA**: A class implementing the OCBA tree policy for MCTS.

- **`TicTacToe-results.ipynb`**:

    - A Jupyter notebook that provides a detailed, step-by-step explanation of the experiment.
    

## Reproducing Results from the Paper

The main objective of this repository is to reproduce and validate the results from the paper [An Optimal Computing Budget Allocation Tree Policy for Monte Carlo Tree Search](https://arxiv.org/pdf/2009.12407). The paper introduces the OCBA tree policy and demonstrates its efficiency in guiding the MCTS algorithm. This repository replicates those experiments in the context of a Tic-Tac-Toe game, comparing the performance of OCBA against the traditional UCB policy.


## License

This project is licensed under the MIT License. See the LICENSE file for more details.
<!-- #endregion -->
