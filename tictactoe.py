import numpy as np
from abc import ABC, abstractmethod


class TicTacToeMove(ABC):
    def __init__(self, x_coordinate, y_coordinate, value):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.value = value

    def __repr__(self):
        return "x:{0} y:{1} v:{2}".format(
            self.x_coordinate,
            self.y_coordinate,
            self.value
        )

class TwoPlayersAbstractGameState(ABC):

    @abstractmethod
    def game_result(self):
        """
        this property should return:

         1 if player #1 wins
        -1 if player #2 wins
         0 if there is a draw
         None if result is unknown

        Returns
        -------
        int

        """
        pass

    @abstractmethod
    def is_game_over(self):
        """
        boolean indicating if the game is over,
        simplest implementation may just be
        `return self.game_result() is not None`

        Returns
        -------
        boolean

        """
        pass

    @abstractmethod
    def move(self, action):
        """
        consumes action and returns resulting TwoPlayersAbstractGameState

        Parameters
        ----------
        action: AbstractGameAction

        Returns
        -------
        TwoPlayersAbstractGameState

        """
        pass

    @abstractmethod
    def get_legal_actions(self):
        """
        returns list of legal action at current game state
        Returns
        -------
        list of AbstractGameAction

        """
        pass


class TicTacToeGameState(TwoPlayersAbstractGameState):

    def __init__(self, state, player=1):
        if len(state.shape) != 2 or state.shape[0] != state.shape[1]:
            raise ValueError("Only 2D square boards allowed")
        self.board = state
        self.board_size = state.shape[0]
        self.player = player

        self.first_player_o = 1
        self.second_player_x = -1


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
        # check if game is over
        rowsum = np.sum(self.board, 0)
        colsum = np.sum(self.board, 1)
        diag_sum_tl = self.board.trace()
        diag_sum_tr = self.board[::-1].trace()

        player_one_wins = any(rowsum == self.board_size)
        player_one_wins += any(colsum == self.board_size)
        player_one_wins += (diag_sum_tl == self.board_size)
        player_one_wins += (diag_sum_tr == self.board_size)

        if player_one_wins:
            return self.first_player_o

        player_two_wins = any(rowsum == -self.board_size)
        player_two_wins += any(colsum == -self.board_size)
        player_two_wins += (diag_sum_tl == -self.board_size)
        player_two_wins += (diag_sum_tr == -self.board_size)

        if player_two_wins:
            return self.second_player_x

        if np.all(self.board != 0):
            return 0

        # if not over - no result
        return None

    def is_game_over(self):
        return self.game_result is not None

    def is_move_legal(self, move):
        # check if correct player moves
        if move.value != self.player:
            return False

        # check if inside the board on x-axis
        x_in_range = (0 <= move.x_coordinate < self.board_size)
        if not x_in_range:
            return False

        # check if inside the board on y-axis
        y_in_range = (0 <= move.y_coordinate < self.board_size)
        if not y_in_range:
            return False

        # finally check if board field not occupied yet
        return self.board[move.x_coordinate, move.y_coordinate] == 0

    def move(self, move):
        if not self.is_move_legal(move):
            raise ValueError(
                "move {0} on board {1} is not legal". format(move, self.board)
            )
        new_board = np.copy(self.board)
        new_board[move.x_coordinate, move.y_coordinate] = move.value
        if self.player == self.first_player_o:
            player = self.second_player_x
        else:
            player = self.first_player_o

        new_state = TicTacToeGameState(new_board, player)
        return new_state

    def get_legal_actions(self):
        indices = np.where(self.board == 0)
        return [
            TicTacToeMove(coords[0], coords[1], self.player)
            for coords in list(zip(indices[0], indices[1]))
        ]

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
