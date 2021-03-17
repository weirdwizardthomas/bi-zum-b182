import time
import numpy as np

EMPTY_TILE_TOKEN = '.'
PLAYER_2_TOKEN = 'O'
PLAYER_1_TOKEN = 'X'

MAX_DEPTH = 4  # maximal depth of the game tree
MAX_STEP_TIME = 0.5  # maximal length of each step's calculation, in seconds


class Game:
    """
    The Tic-Tac-Toe's game logic.

    Attributes
    ----------
    board: 2-D matrix of strings
        A square 2-D matrix of string tokens that represented the current board state. Tokens are one of:
        EMPTY_TILE_TOKEN
        PLAYER_1_TOKEN
        PLAYER_2_TOKEN
    board_size: int
        number of columns/number of rows of the board
    tiles_set: int
        counter of how many tiles have been set, i.e. are not EMPTY_TILE_TOKEN but are PLAYER_1_TOKEN or PLAYER_2_TOKEN
    players: dict
        Dictionary of players and the action they take on their turn. Player 1 is always minimising,
        Player 2 is always maximising.
    player_turn: str
        Token of the player that is currently playing
    timer_start: int
        timestamp of when a given exploration of possible moves started
    """

    def __init__(self, size: int, players: int):
        self.board = np.full((size, size), EMPTY_TILE_TOKEN, dtype=str)
        self.board_size = size
        self.tiles_set = 0
        self.timer_start = None

        self.player_turn = PLAYER_1_TOKEN
        # player 1 is always minimising, player 2 is always maximising
        self.players = {PLAYER_1_TOKEN: self.__min, PLAYER_2_TOKEN: self.__max}
        if players == 2:
            self.players[PLAYER_1_TOKEN] = self.__get_player_input
            self.players[PLAYER_2_TOKEN] = self.__get_player_input
        elif players == 1:
            self.players[PLAYER_1_TOKEN] = self.__get_player_input

    def __draw_board(self):
        """
        Draws the board to the console
        :return: None
        """
        VERTICAL_WALL = '|'
        HORIZONTAL_WALL = '-'

        print('    ', end='')
        for i in range(self.board_size):
            print(i, end=' ')
        print('\n ', '-' * (2 * self.board_size + 3))
        i = 0
        for row in self.board:
            print(i, VERTICAL_WALL, ' '.join(row), VERTICAL_WALL)
            i += 1
        print(' ', HORIZONTAL_WALL * (2 * self.board_size + 3))

    def __move_is_valid(self, x: int, y: int):
        """
        Determines whether the tile at given coordinates is available to mark
        :param x: X-coordinate of the tile
        :param y: Y-coordinate of the tile
        :return: True if the move is in bounds and valid, False otherwise
        """
        return 0 <= x < self.board_size and 0 <= y < self.board_size and self.board[x][y] == EMPTY_TILE_TOKEN

    def __score_board(self):
        """
        A heuristic that evaluates the current state of the game.
        The more the board is in favour of player 1, the smaller the number is, and bigger for player 2.
        :return: Number representing in whose favour the board is.
        """
        score = 0
        player_counters = {PLAYER_1_TOKEN: 0, PLAYER_2_TOKEN: 0, EMPTY_TILE_TOKEN: 0}

        # row by row
        for x in range(self.board_size):
            self.__reset_scoring_counters(player_counters)
            for y in range(self.board_size):
                tile = self.board[x][y]
                player_counters[tile] += 1
            score = self.__score_line(player_counters, score)

        # column by column
        for y in range(self.board_size):
            self.__reset_scoring_counters(player_counters)
            for x in range(self.board_size):
                tile = self.board[x][y]
                player_counters[tile] += 1
            score = self.__score_line(player_counters, score)

        # top left to bottom right diagonal
        self.__reset_scoring_counters(player_counters)
        for x in range(self.board_size):
            tile = self.board[x][x]
            player_counters[tile] += 1
        score = self.__score_line(player_counters, score)

        # top right to bottom left diagonal
        self.__reset_scoring_counters(player_counters)
        for x in range(self.board_size):
            tile = self.board[x][self.board_size - 1 - x]
            player_counters[tile] += 1
        score = self.__score_line(player_counters, score)

        return score

    @staticmethod
    def __score_line(player_counters: dict, score: int):
        """
        Calculates the score of a single line - domination of either player.
        :param player_counters: Player token counts in the given line
        :param score: Current score
        :return: Current score updated by the score of the line
        """
        if player_counters[PLAYER_1_TOKEN] == 0 and player_counters[PLAYER_2_TOKEN] == 0:
            pass
        elif player_counters[PLAYER_1_TOKEN] == 0:
            score += 10 ** (player_counters[PLAYER_2_TOKEN] - 1)
        elif player_counters[PLAYER_2_TOKEN] == 0:
            score += -10 ** (player_counters[PLAYER_1_TOKEN] - 1)

        return score

    @staticmethod
    def __reset_scoring_counters(player_counters: dict):
        """
        Sets the counters for each token to their default value (0)
        :param player_counters: Player token counts in the given line
        :return: None
        """
        player_counters[PLAYER_1_TOKEN] = 0
        player_counters[PLAYER_2_TOKEN] = 0
        player_counters[EMPTY_TILE_TOKEN] = 0

    def __game_over(self):
        """
        Determines whether whether the game is over and if it is, which player won the game
        :return: None if the game is not over yet, EMPTY_TILE_TOKEN if the game is a tie,
                 PLAYER_1_TOKEN if player 1 won, PLAYER_2_TOKEN if player 2 won
        """

        # container for the result of each line ( columns, rows + diagonals)
        lines = np.zeros(2 + 2 * self.board_size, dtype=int)

        i = 0
        # left top to right bottom diagonal
        for x in range(self.board_size):
            if self.board[x][x] == PLAYER_1_TOKEN:
                lines[i] += 1
            elif self.board[x][x] == PLAYER_2_TOKEN:
                lines[i] -= 1
        i += 1

        # right top to left bottom diagonal
        for x in range(self.board_size):
            y = self.board_size - 1 - x
            if self.board[x][y] == PLAYER_1_TOKEN:
                lines[i] += 1
            elif self.board[x][y] == PLAYER_2_TOKEN:
                lines[i] -= 1
        i += 1

        # rows
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] == PLAYER_1_TOKEN:
                    lines[i] += 1
                elif self.board[x][y] == PLAYER_2_TOKEN:
                    lines[i] -= 1
            i += 1

        # columns
        for y in range(self.board_size):
            for x in range(self.board_size):
                if self.board[x][y] == PLAYER_1_TOKEN:
                    lines[i] += 1
                elif self.board[x][y] == PLAYER_2_TOKEN:
                    lines[i] -= 1
            i += 1

        for line in lines:
            if line == self.board_size:
                return PLAYER_1_TOKEN
            if line == -self.board_size:
                return PLAYER_2_TOKEN

        # is board empty?
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] == EMPTY_TILE_TOKEN:
                    return None

        return EMPTY_TILE_TOKEN

    def __max(self, depth: int = 0, alpha: float = -np.math.inf, beta: float = np.math.inf):
        """
        Maximising agent of the minimax algorithm.
        Evaluates children on its level and picks the biggest one.

        Terminating conditions:
            a) game is over, i.e. no possible moves left
            b) maximum depth of the tree has been reached (MAX_DEPTH)
            c) time limit for the turn has been reached (MAX_STEP_TIME)
        :param depth: Current tree depth
        :param alpha: Alpha value of the minimax algorithm
        :param beta: Beta value of the minimax algorithm
        :return: tuple of best choice's score,  best choice's x-coordinate, best choice's y-coordinate
        """
        biggest_value = -np.math.inf
        best_x, best_y = None, None

        game_over = self.__game_over()
        timer_now = time.time() - self.timer_start

        # terminating conditions
        if depth >= MAX_DEPTH or game_over is not None or timer_now >= MAX_STEP_TIME:
            return self.__score_board(), best_x, best_y

        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.__move_is_valid(x, y):
                    self.board[x][y] = PLAYER_2_TOKEN
                    value, _, _ = self.__min(depth + 1, alpha, beta)
                    if value > biggest_value:
                        biggest_value = value
                        best_x, best_y = x, y

                    # reset the tile
                    self.board[x][y] = EMPTY_TILE_TOKEN

                    if biggest_value >= beta:
                        return biggest_value, x, y

                    alpha = max(biggest_value, alpha)

        return biggest_value, best_x, best_y

    def __min(self, depth: int = 0, alpha: float = - np.math.inf, beta: float = np.math.inf):
        """
        Minimisng agent of the minimax algorithm.
        Evaluates children on its level and picks the smallest one.

        Terminating conditions:
            a) game is over, i.e. no possible moves left
            b) maximum depth of the tree has been reached (MAX_DEPTH)
            c) time limit for the turn has been reached (MAX_STEP_TIME)

        :param depth: Current tree depth
        :param alpha: Alpha value of the minimax algorithm
        :param beta: Beta value of the minimax algorithm
        :return: tuple of best choice's score,  best choice's x-coordinate, best choice's y-coordinate
        """
        smallest_value = np.math.inf
        best_x, best_y = None, None

        timer_now = time.time() - self.timer_start
        game_over = self.__game_over()

        # terminating condition
        if depth >= MAX_DEPTH or game_over is not None or timer_now >= MAX_STEP_TIME:
            return self.__score_board(), best_x, best_y

        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.__move_is_valid(x, y):
                    self.board[x][y] = PLAYER_1_TOKEN
                    value, _, _ = self.__max(depth + 1, alpha, beta)
                    if value < smallest_value:
                        smallest_value = value
                        best_x, best_y = x, y

                    self.board[x][y] = EMPTY_TILE_TOKEN

                    if smallest_value <= alpha:
                        return smallest_value, x, y

                    beta = min(smallest_value, beta)

        return smallest_value, best_x, best_y

    def __play(self, x: int, y: int, token: str):
        """
        Places a player token at specified coordinates. Assumes the move is valid,
        i.e. the coordinates are bound & the tile is not occupied yet.
        :param x: x-coordinate of the tile
        :param y: y-coordinate of the tile
        :param token: Player token to place
        :return: None
        """
        self.board[x][y] = token
        self.tiles_set += 1

    def __get_player_input(self):
        """
        Queries the user for a move input via console.
        :return: tuple of None, player chosen x-coordinate, player chosen y-coordinate
        """
        answer = []
        while len(answer) != 2:
            answer = input("Enter [x,y] coordinates:")
            answer = answer.strip().split(' ')
            try:
                x, y = int(answer[0]), int(answer[1])
                if not self.__move_is_valid(x, y):
                    print("Invalid coordinates, try again:")
                    answer = []
            except (ValueError, IndexError):
                answer = []
                print("Invalid coordinates, try again:")

        return None, x, y

    def __swap_players(self):
        """
        Changes the player who is currently playing
        :return: None
        """
        self.player_turn = PLAYER_1_TOKEN if self.player_turn == PLAYER_2_TOKEN else PLAYER_2_TOKEN

    def play(self):
        """
        Runs the game.
        :return: None
        """
        while True:
            self.__draw_board()
            game_over = self.__game_over()

            # Printing the appropriate message if the game has ended
            if game_over is not None:
                print("Tie") if game_over == EMPTY_TILE_TOKEN else print(game_over, 'wins!')
                break

            # set timer
            self.timer_start = time.time()
            # get coordinates of the turn
            _, x, y = self.players[self.player_turn]()
            print("Evaluation time ", time.time() - self.timer_start, "s")
            # place token
            self.__play(x, y, self.player_turn)
            self.__swap_players()
