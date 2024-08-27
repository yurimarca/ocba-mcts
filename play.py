import matplotlib.pyplot as plt
import numpy as np
import random

class TicTacToeGameState():

    def __init__(self, board_state=None, player=1):
        self.first_player_o = 1
        self.second_player_x = -1

        #if player != self.first_player_o or player != self.second_player_x:
        #    print(player)
        #    raise ValueError(f"Player can only be {self.first_player_o} or {self.second_player_x}.")
            
        if board_state is None:
            self.board = np.zeros((3,3))
        else:
            assert board_state.shape == (3,3), "Board size error!"
            self.board = board_state
            
        
        self.player = player
        print(self.player)

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
        x,y = self.map_move_to_board(move)
        return self.board[x, y] == 0

    def move(self, move):
        x,y = self.map_move_to_board(move)
        
        if not self.is_move_legal(move):
            raise ValueError(
                "move {0} on board {1} is not legal". format(move, self.board)
            )

        new_board = np.copy(self.board)
        new_board[x, y] = self.player

        print(new_board.shape)

        return TicTacToeGameState(new_board, self.next_player)

    def get_legal_actions(self):
        return [i * 3 + j + 1 for i in range(3) for j in range(3) if self.board[i, j] == 0]
    
    def is_terminal(self):
        for i in range(3):
            if abs(sum(self.board[i, :])) == 3 or abs(sum(self.board[:, i])) == 3:
                return True
        if abs(sum([self.board[i, i] for i in range(3)])) == 3 or abs(sum([self.board[i, 2 - i] for i in range(3)])) == 3:
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
        pos = 0
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

class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0

    def is_fully_expanded(self):
        return len(self.children) == len(self.state.get_legal_actions())

    def best_child(self, exploration_weight=1.4):
        choices_weights = [
            (child.value / child.visits) + exploration_weight * np.sqrt(np.log(self.visits) / child.visits)
            for child in self.children
        ]
        return self.children[np.argmax(choices_weights)]

    def expand(self):
        legal_actions = self.state.get_legal_actions()
        action = random.choice([a for a in legal_actions if a not in [child.state.board for child in self.children]])
        next_state = self.state.move(action)
        child_node = MCTSNode(next_state, parent=self)
        self.children.append(child_node)
        return child_node

    def update(self, value):
        self.visits += 1
        self.value += value

class MCTS:
    def __init__(self, num_simulations=1000):
        self.num_simulations = num_simulations

    def search(self, root):
        for _ in range(self.num_simulations):
            node = self._select(root)
            value = self._simulate(node)
            self._backpropagate(node, value)
        return root.best_child(0).state

    def _select(self, node):
        while not node.state.is_game_over():
            if node.is_fully_expanded():
                node = node.best_child()
            else:
                return node.expand()
        return node

    def _simulate(self, node):
        current_state = node.state
        while not current_state.is_game_over():
            action = random.choice(current_state.get_legal_actions())
            current_state = current_state.move(action)
        return current_state.game_result

    def _backpropagate(self, node, value):
        while node is not None:
            node.update(value)
            node = node.parent


game_state = TicTacToeGameState()

print("Welcome to Tic-Tac-Toe!")
print("The board positions are numbered 1 through 9 as follows:")
game_state.print_board_positions()

while not game_state.is_game_over():
    print("\nCurrent board:")
    game_state.print_board()
    
    move = None
    while move is None:
        try:
            move = int(input(f"Player {'O' if game_state.player == 1 else 'X'}, enter your move (1-9): "))
            if move < 1 or move > 9 or not game_state.is_move_legal(move):
                raise ValueError
        except ValueError:
            print("Invalid move. Please enter a number from 1 to 9 corresponding to an empty space on the board.")
            move = None
    
    game_state = game_state.move(move)

print("\nFinal board:")
game_state.print_board()

result = game_state.game_result
if result == 1:
    print("Player O wins!")
elif result == -1:
    print("Player X wins!")
else:
    print("It's a draw!")
