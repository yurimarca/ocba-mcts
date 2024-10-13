import matplotlib.pyplot as plt
import numpy as np
import random

from graphviz import Digraph

class TicTacToeGameState():

    def __init__(self, board_state=None, player=1):
        self.first_player_o = 1
        self.second_player_x = -1

        if board_state is None:
            self.board = np.zeros((3, 3))
        else:
            assert board_state.shape == (3, 3), "Board size error!"
            self.board = board_state

        self.player = player

        #self.print_board()

    def __repr__(self):
        ret_string = self.draw_board()
        ret_string += 'Next to move: '
        if self.player == self.first_player_o:
            ret_string += 'O'
        elif self.player == self.second_player_x:
            ret_string += 'X'

        return ret_string

    @property
    def game_result(self):
        # Check if game is over
        rowsum = np.sum(self.board, 0)
        colsum = np.sum(self.board, 1)
        diag_sum_tl = self.board.trace()
        diag_sum_tr = self.board[::-1].trace()

        player_one_wins = any(rowsum == 3)
        player_one_wins += any(colsum == 3)
        player_one_wins += (diag_sum_tl == 3)
        player_one_wins += (diag_sum_tr == 3)

        if player_one_wins:
            return self.first_player_o

        player_two_wins = any(rowsum == -3)
        player_two_wins += any(colsum == -3)
        player_two_wins += (diag_sum_tl == -3)
        player_two_wins += (diag_sum_tr == -3)

        if player_two_wins:
            return self.second_player_x

        if np.all(self.board != 0):
            return 0

        # If not over - no result
        return None

    def is_game_over(self):
        return self.game_result is not None

    @property
    def next_player(self):
        return -self.player

    def map_move_to_board(self, move):
        if move < 1 or move > 9:
            raise ValueError("Move must be between 1 and 9.")
        row = (move - 1) // 3
        col = (move - 1) % 3

        return [row, col]

    def is_move_legal(self, move):
        x, y = self.map_move_to_board(move)
        return self.board[x, y] == 0

    def move(self, move):
        x, y = self.map_move_to_board(move)

        if not self.is_move_legal(move):
            raise ValueError(
                "move {0} on board {1} is not legal".format(move, self.board)
            )

        new_board = np.copy(self.board)
        new_board[x, y] = self.player

        #print(f"\nMove: {move} by Player {'O' if self.player == 1 else 'X'}")
        #print("Board after move:")

        return TicTacToeGameState(new_board, self.next_player)

    def get_legal_actions(self):
        return [i * 3 + j + 1 for i in range(3) for j in range(3) if self.board[i, j] == 0]

    def is_terminal(self):
        for i in range(3):
            if abs(sum(self.board[i, :])) == 3 or abs(sum(self.board[:, i])) == 3:
                return True
        if abs(sum([self.board[i, i] for i in range(3)])) == 3 or abs(
                sum([self.board[i, 2 - i] for i in range(3)])) == 3:
            return True
        return np.all(self.board != 0)

    def get_winner(self):
        if self.is_terminal():
            for i in range(3):
                if abs(sum(self.board[i, :])) == 3:
                    return self.board[i, 0]
                if abs(sum(self.board[:, i])) == 3:
                    return self.board[0, i]
            if abs(sum([self.board[i, i] for i in range(3)])) == 3:
                return self.board[0, 0]
            if abs(sum([self.board[i, 2 - i] for i in range(3)])) == 3:
                return self.board[0, 2]
        return 0

    def draw_tictactoe_board(self, step, save_path=None, show=False):
        fig, ax = plt.subplots()
        ax.axis('off')

        # Draw the grid
        ax.set_xlim(0, 3)
        ax.set_ylim(0, 3)

        for i in range(1, 3):
            ax.plot([i, i], [0, 3], color='black')
            ax.plot([0, 3], [i, i], color='black')

        # Draw X's and O's
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == self.first_player_o:
                    ax.text(j + 0.5, 2.5 - i, 'O', fontsize=40, ha='center', va='center', color='red')
                elif self.board[i][j] == self.second_player_x:
                    ax.text(j + 0.5, 2.5 - i, 'X', fontsize=40, ha='center', va='center', color='blue')

        # Set title
        ax.set_title(f'Step: {step}')

        # Save the figure if a save path is provided
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')

        # Show the figure if in debug mode
        if show:
            plt.show()

        # Close the plot to avoid display issues when generating many figures
        plt.close(fig)

        return fig

    def draw_board(self):
        board_string = ''
        for i in range(self.board.shape[0]):
            board_string += '\n'
            if i > 0:
                for j in range(self.board.shape[1]):
                    if (j == 0) or (j == self.board.shape[1] - 1):
                        board_string += '--'
                    else:
                        board_string += '---'
                    if j < self.board.shape[1] - 1:
                        board_string += '+'
                    else:
                        board_string += '\n'
            for j in range(self.board.shape[1]):
                if self.board[i][j] == 0:
                    board_string += ' '
                elif self.board[i][j] == self.first_player_o:
                    board_string += 'O'
                elif self.board[i][j] == self.second_player_x:
                    board_string += 'X'
                if j < self.board.shape[1] - 1:
                    board_string += ' | '
        board_string += '\n'
        board_string += '\n'

        return board_string

    def print_board(self):
        print(self.draw_board())

    def print_board_positions(self):
        pos = 1
        for i in range(self.board.shape[0]):
            print()
            if i > 0:
                for j in range(self.board.shape[1]):
                    if (j == 0) or (j == self.board.shape[1] - 1):
                        print('--', end='')
                    else:
                        print('---', end='')
                    if j < self.board.shape[1] - 1:
                        print('+', end='')
                    else:
                        print()
            for j in range(self.board.shape[1]):
                print(str(pos), end='')
                pos += 1
                if j < self.board.shape[1] - 1:
                    print(' | ', end='')

        print()
        print()

class Node():
    _node_counter = 0  # Class variable to keep track of node IDs

    def __init__(self, state, action=None, depth=0, parent=None):
        self._id = Node._node_counter
        Node._node_counter += 1
        self.state = state
        self.action = action  # Store the action that led to this state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0
        self.depth = depth
        self._untried_actions = None
        self._state_hash = self.hash_state()

    def hash_state(self):
        """ Hashes the board state to be used for detecting repeated states. """
        return tuple(self.state.board.flatten())

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    @property
    def untried_actions(self):
        if self._untried_actions is None:
            self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions

    def best_child(self, exploration_weight=1.4):
        """ Use the UCB1 formula to select the best child node. """
        choices_weights = [
            (child.value / child.visits) + exploration_weight * np.sqrt(np.log(self.visits) / child.visits)
            for child in self.children
        ]
        return self.children[np.argmax(choices_weights)]

    def expand(self):
        # Choose an action to expand
        action = self.prioritize_action(self.untried_actions)
        next_state = self.state.move(action)
        child_depth = self.depth + 1
        # Create a new child node, optionally storing the action
        child_node = Node(next_state, action=action, parent=self, depth=child_depth)
        self.untried_actions.remove(action)
        self.children.append(child_node)
        return child_node

    def prioritize_action(self, actions):
        """ Prioritize actions that could lead to winning or blocking an opponent's win. """
        for action in actions:
            temp_state = self.state.move(action)
            if temp_state.game_result == self.state.player:  # Winning move
                return action
            elif temp_state.game_result == -self.state.player:  # Blocking move
                return action
        # If no winning/blocking move, return random
        return random.choice(actions)

    def update(self, value):
        self.visits += 1
        self.value += value

    def plot_first_layer(self, graph):
        # Create a unique node label for the current node
        label = f"ID: {self._id}\nValue: {self.value:.2f}\nVisits: {self.visits}"
        label += f"\n{self.state.draw_board()}"

        # Use both _id and depth to create a unique node name
        node_name = f"{self.depth}-{self._id}"

        # Add the root node to the graph
        graph.node(node_name, label)

        # Sort children based on _id
        self.children.sort(key=lambda child: child._id)

        # Plot only the first layer of children
        for child in self.children:
            child_label = f"ID: {child._id}\nValue: {child.value:.2f}\nVisits: {child.visits}"
            child_label += f"\n{child.state.draw_board()}"
            child_node_name = f"{child.depth}-{child._id}"  # Unique name using depth and _id
            graph.node(child_node_name, child_label)
            graph.edge(node_name, child_node_name)

    def plot_full_tree(self, graph):
        # Create a unique node label for the current node
        label = f"ID: {self._id}\nAction: {self.action}\nValue: {self.value:.2f}\nVisits: {self.visits}"
        label += f"\n{self.state.draw_board()}"

        # Use the unique _id to create a unique node name
        node_name = f"Node_{self._id}"

        # Add the current node to the graph
        graph.node(node_name, label)

        # Recursively plot each child node and its subtree
        for child in self.children:
            child.plot_full_tree(graph)
            child_node_name = f"Node_{child._id}"
            graph.edge(node_name, child_node_name)


class MCTS:
    def __init__(self, player, num_simulations=200):
        self.num_simulations = num_simulations
        self.player = player

    def search(self, root):
        for i in range(self.num_simulations):
            node, path = self._select(root)
            value = self._simulate(node)
            self._backpropagate(node, value)
            # Call the plot_tree_rollout function
            #self.plot_tree_rollout(root, path, iteration=i)
        # Optionally, plot the full tree after all simulations
        self.plot_full_tree(root)
        return root.best_child(0).state

    def _select(self, node):
        """ Select until we find an unexpanded node or terminal node.
            Keep track of the nodes visited during selection.
        """
        path = [node]
        while not node.state.is_game_over():
            if node.is_fully_expanded():
                node = node.best_child()
                path.append(node)
            else:
                new_node = node.expand()
                path.append(new_node)
                return new_node, path
        return node, path

    def _simulate(self, node):
        """ Simulate a random rollout from the node. """
        current_env_state = node.state

        while not current_env_state.is_game_over():
            possible_moves = current_env_state.get_legal_actions()
            action = self._rollout(possible_moves)
            current_env_state = current_env_state.move(action)

        if current_env_state.game_result == -node.state.player:
            return 1
        elif current_env_state.game_result == 0:
            return 0.5
        else:
            return -1

    def _rollout(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]

    def _backpropagate(self, node, value):
        """ Backpropagate and negate value for alternate players. """
        while node is not None:
            node.update(value)
            value = -value
            node = node.parent

    def plot_tree_rollout(self, root, rollout_path, iteration):
        graph = Digraph()
        self._plot_tree_with_rollout(root, rollout_path, graph)
        file_name = f'mcts_tree_rollout_{iteration}'
        graph.render(file_name, format='png', cleanup=True)

    def _plot_tree_with_rollout(self, node, rollout_path, graph):
        # Create a unique node label
        label = f"ID: {node._id}\nValue: {node.value:.2f}\nVisits: {node.visits}"
        label += f"\n{node.state.draw_board()}"

        node_name = f"Node_{node._id}"

        # Check if node is in the rollout path
        if node in rollout_path:
            graph.node(node_name, label, color='red', fontcolor='red')
        else:
            graph.node(node_name, label)

        for child in node.children:
            child_node_name = f"Node_{child._id}"
            graph.edge(node_name, child_node_name)
            # Recursive call
            self._plot_tree_with_rollout(child, rollout_path, graph)

    def plot_full_tree(self, root, file_name='mcts_tree_full'):
        graph = Digraph()
        self._plot_full_tree_helper(root, graph)
        graph.render(file_name, format='pdf', cleanup=True)

    def _plot_full_tree_helper(self, node, graph):
        # Create a unique node label for the current node
        label = f"ID: {node._id}\nValue: {node.value:.2f}\nVisits: {node.visits}"
        label += f"\n{node.state.draw_board()}"

        # Use the unique _id to create a unique node name
        node_name = f"Node_{node._id}"

        # Add the current node to the graph
        graph.node(node_name, label)

        for child in node.children:
            child_node_name = f"Node_{child._id}"
            graph.edge(node_name, child_node_name)
            # Recursive call
            self._plot_full_tree_helper(child, graph)

random_seed = 42

# Set the random seeds for reproducibility
np.random.seed(random_seed)
random.seed(random_seed)

# Initialize game state with player X (-1) moving first
game_state = TicTacToeGameState(player=-1)

print("Welcome to Tic-Tac-Toe!")
print("The board positions are numbered 1 through 9 as follows:")
game_state.print_board_positions()

mcts = MCTS(player=-1, num_simulations=1000)

while not game_state.is_game_over():
    print("\nCurrent board:")
    game_state.print_board()

    if game_state.player == 1:  # Human's turn
        move = None
        while move is None:
            try:
                move = int(input(f"Player O, enter your move (1-9): "))
                if move < 1 or move > 9 or not game_state.is_move_legal(move):
                    raise ValueError
            except ValueError:
                print("Invalid move. Please enter a number from 1 to 9 corresponding to an empty space on the board.")
                move = None
        game_state = game_state.move(move)
    else:  # MCTS Agent's turn
        print("MCTS Agent is thinking...")
        root = Node(game_state)

        game_state = mcts.search(root)

print("\nFinal board:")
game_state.print_board()

result = game_state.game_result
if result == 1:
    print("Player O wins!")
elif result == -1:
    print("Player X (MCTS) wins!")
else:
    print("It's a draw!")

# # After running MCTS search
# game_state = TicTacToeGameState(player=-1)
# mcts = MCTS(player=-1, num_simulations=200)
# root = Node(game_state)
# mcts.search(root)
# mcts.plot_full_tree(root, file_name='mcts_tree_full')
