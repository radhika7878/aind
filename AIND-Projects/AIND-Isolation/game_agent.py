"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import math


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_moves = len(game.get_legal_moves(player))
    enemy_moves = len(game.get_legal_moves(game.get_opponent(player)))
    # If number of moves is different return the difference
    if my_moves != enemy_moves:
        return float(my_moves - enemy_moves)
    # Else look for positional advantage: who is closer to centre and hence has more degrees of freedom
    else:
        cx, cy = game.width/2. , game.height/2.
        my, mx = game.get_player_location(player)
        ey, ex = game.get_player_location(game.get_opponent(player))
        my_dist = abs(mx - cx) + abs(my - cy)
        enemy_dist = abs(ex - cx) + abs(ey - cy)
        return float(enemy_dist - my_dist)


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    my_moves = len(game.get_legal_moves(player))
    enemy_moves = len(game.get_legal_moves(game.get_opponent(player)))
    cx, cy = game.width/2. , game.height/2.
    my, mx = game.get_player_location(player)
    ey, ex = game.get_player_location(game.get_opponent(player))
    my_dist_to_center = float((cy - my)**2 + (cx - mx)**2)
    enemy_dist_to_center = float((cy - ey)**2 + (cx - ex)**2)
    return float((my_moves - enemy_moves) + (enemy_dist_to_center - my_dist_to_center)/(2*game.move_count))


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    my_moves = len(game.get_legal_moves(player))
    enemy_moves = len(game.get_legal_moves(game.get_opponent(player)))
    my, mx = game.get_player_location(player)
    cx, cy = game.width/2. , game.height/2.
    jumps_to_center = min(abs(mx - cx) , abs(my - cy))
    return (2*my_moves - enemy_moves - 0.5*jumps_to_center)




class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def __min_value(self, game, depth):
        self.__timer()
        if self.__terminal_test(game , depth):
            return self.score(game, self)
        poss_moves = game.get_legal_moves()
        min_val = float("inf")
        for move in poss_moves:
            new_gameState = game.forecast_move(move)
            min_val = min(min_val, self.__max_value(new_gameState, depth-1))
        return min_val

    def __max_value(self, game, depth):
        self.__timer()
        if self.__terminal_test(game , depth):
            return self.score(game, self)
        poss_moves = game.get_legal_moves()
        max_val = float("-inf")
        for move in poss_moves:
            new_gameState = game.forecast_move(move)
            max_val = max(max_val, self.__min_value(new_gameState, depth-1))
        return max_val

    def __terminal_test(self, game, depth):
        self.__timer()
        if len(game.get_legal_moves()) != 0  and depth > 0:
            return False
        return True

    def __timer(self):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        self.__timer()
        poss_moves = game.get_legal_moves()
        if not poss_moves:
            return (-1, -1)
        # vals = [(self.__min_value.(game.forecast_move(m), depth - 1), m) for m in poss_moves]
        # _, move = max(vals)
        # return move
        return max(poss_moves,
               key=lambda m: self.__min_value(game.forecast_move(m), depth - 1))

        


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        poss_moves = game.get_legal_moves(self)
        if len(poss_moves) > 0:
            best_move = poss_moves[0]
        else:
            best_move = (-1, -1)
        try:
            depth =1
            while True:
                curr_move = self.alphabeta(game, depth)
                if curr_move == (-1, -1):
                    return best_move
                else:
                    best_move = curr_move
                depth += 1
        except SearchTimeout:
            return best_move
        return best_move

    def __min_value(self, game, depth, alpha, beta):
        self.__timer()
        curr_best_move = (-1, -1)
        if self.__terminal_test(game , depth):
            return (self.score(game, self), curr_best_move)
        poss_moves = game.get_legal_moves()
        min_val = float("inf")
        for move in poss_moves:
            ans = self.__max_value(game.forecast_move(move), depth-1, alpha, beta)
            if ans[0] < min_val:
                min_val, _  = ans
                curr_best_move = move
            if min_val <= alpha:
                return (min_val, curr_best_move)
            beta = min(beta, min_val)
        return (min_val, curr_best_move)

    def __max_value(self, game, depth, alpha, beta):
        self.__timer()
        curr_best_move  = (-1, -1)
        if self.__terminal_test(game , depth):
            return (self.score(game, self), curr_best_move)
        poss_moves = game.get_legal_moves()
        max_val = float("-inf")
        for move in poss_moves:
            ans = self.__min_value(game.forecast_move(move), depth-1, alpha, beta)
            if ans[0] > max_val:
                max_val, _  = ans
                curr_best_move = move
            if max_val >= beta:
                return (max_val, curr_best_move)
            alpha = max(alpha, max_val)
        return (max_val, curr_best_move)

    def __terminal_test(self, game, depth):
        self.__timer()
        if len(game.get_legal_moves()) != 0  and depth > 0:
            return False
        return True

    def __timer(self):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        self.__timer()
        _, move = self.__max_value(game, depth, alpha, beta)
        return move
