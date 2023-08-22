from OthelloBoard import *


class Player:
    """Base player class"""

    def __init__(self, symbol):
        self.symbol = symbol

    def get_symbol(self):
        return self.symbol

    def get_move(self, board):
        raise NotImplementedError()


class HumanPlayer(Player):
    """Human subclass with text input in command line"""

    def __init__(self, symbol):
        Player.__init__(self, symbol)
        self.total_nodes_seen = 0

    def clone(self):
        return HumanPlayer(self.symbol)

    def get_move(self, board):
        col = int(input("Enter col:"))
        row = int(input("Enter row:"))
        return (col, row)


class AlphaBetaPlayer(Player):
    """Class for Alphabeta AI: implement functions minimax, eval_board, get_successors, get_move
    eval_type: int
        0 for H0, 1 for H1, 2 for H2
    prune: bool
        1 for alpha-beta, 0 otherwise
    max_depth: one move makes the depth of a position to 1, search should not exceed depth
    total_nodes_seen: used to keep track of the number of nodes the algorithm has seearched through
    symbol: X for player 1 and O for player 2
    """

    def __init__(self, symbol, eval_type, prune, max_depth):
        Player.__init__(self, symbol)
        self.eval_type = eval_type
        self.prune = prune
        self.max_depth = int(max_depth)
        self.max_depth_seen = 0
        self.total_nodes_seen = 0
        if symbol == 'X':
            self.oppSym = 'O'
        else:
            self.oppSym = 'X'

    def terminal_state(self, board):
        # If either player can make a move, it's not a terminal state
        for c in range(board.cols):
            for r in range(board.rows):
                if board.is_legal_move(c, r, "X") or board.is_legal_move(c, r, "O"):
                    return False
        return True

    def terminal_value(self, board):
        # Regardless of X or O, a win is float('inf')
        state = board.count_score(self.symbol) - board.count_score(self.oppSym)
        if state == 0:
            return 0
        elif state > 0:
            return float('inf')
        else:
            return -float('inf')

    def flip_symbol(self, symbol):
        # Short function to flip a symbol
        if symbol == "X":
            return "O"
        else:
            return "X"

    def alphabeta(self, board):
        # Write minimax function here using eval_board and get_successors
        # type:(board) -> (int, int)
        col, row = 0, 0
        alpha = float('-inf')
        beta = float('inf')

        board.value = self.max_value(board, alpha, beta, self.max_depth)

        # How do we pick the successor associated with a max value?
        # We go through the children of the board and find the one
        # that contains the max value. Once we have that, we return the move associated with it.
        for child in board.children:
            if (child.value == board.value):
                col, row = child.move
                break

        return (col, row)

    def max_value(self, board, alpha, beta, remaining_depth):
        # Every time we traverse to max or min, we should increment
        # the total node seen metric.
        self.total_nodes_seen += 1

        # Maximum depth seen is the total
        # max depth minus the remaining depth.
        self.max_depth_seen = max(
            self.max_depth_seen, self.max_depth - remaining_depth)

        # If we're at the terminal position, return the evaluation function of the board.
        if (self.terminal_state(board)):
            board.value = self.terminal_value(board)
            return board.value

        elif (remaining_depth == 0):
            # We evaluate the utility of a non-terminal node and use that
            # to make the best decision.
            board.value = self.eval_board(board)
            return board.value

        # Set initial value for value of current node.
        board.value = float('-inf')

        # Then we explore the successors and do a DFS on each.
        # We should also append the successor states to the parent
        # board and assign the final max_value to the parent board.
        for successor in self.get_successors(board, self.symbol):
            # We do a DFS on the successor, and change player_turn to its opposite.
            board.value = max(
                board.value, self.min_value(successor, alpha, beta, remaining_depth - 1))
            # This indicates pruning is an option.
            if (self.prune and board.value >= beta):
                break

            alpha = max(alpha, board.value)

        return board.value

    def min_value(self, board, alpha, beta, remaining_depth):
        # Every time we traverse to max or min, we should increment
        # the total node seen metric.
        self.total_nodes_seen += 1

        # Maximum depth seen is the total
        # max depth minus the remaining depth.
        self.max_depth_seen = max(
            self.max_depth_seen, self.max_depth - remaining_depth)

        if (self.terminal_state(board)):
            board.value = self.terminal_value(board)
            return board.value

        elif (remaining_depth == 0):
            # We evaluate the utility of a non-terminal node and use that
            # to make the best decision.
            board.value = self.eval_board(board)
            return board.value

        board.value = float('inf')
        # Else we explore the successors and do a DFS on each.
        for successor in self.get_successors(board, self.oppSym):
            # We do a DFS on  successor.
            board.value = min(
                board.value, self.max_value(successor, alpha, beta, remaining_depth - 1))

            if (self.prune and board.value <= alpha):
                break

            beta = min(beta, board.value)

        return board.value

    def eval_board(self, board):
        # Write eval function here
        # type:(board) -> (float)
        value = 0
        if self.eval_type == "0" or self.eval_type == 0:
            value = board.count_score(self.symbol) - \
                board.count_score(self.oppSym)

        elif self.eval_type == "1" or self.eval_type == 1:

            value = self.H1(board)

        elif self.eval_type == "2" or self.eval_type == 2:
            # We take player 1's corner discs - danger disks and subtract
            # from that player 2's corner discs minus danger discs for our
            # evaluation function.
            edge_cell_utilities = {
                (0, 0): 1,
                (1, 0): -1,
                (2, 0): -1,
                (3, 0): 1,
                (0, 1): -1,
                (3, 1): -1,
                (0, 2): -1,
                (3, 2): -1,
                (0, 3): 1,
                (1, 3): -1,
                (2, 3): -1,
                (3, 3): 1
            }

            player_total = 0
            opp_total = 0
            for col, row in edge_cell_utilities.keys():
                symbol = board.get_cell(col, row)
                if (symbol != "."):
                    if (symbol == self.symbol):
                        player_total += edge_cell_utilities[(col, row)]
                    else:
                        opp_total += edge_cell_utilities[(col, row)]

            value = player_total - opp_total
    #    value += board.count_score(self.symbol) - \
    #             board.count_score(self.oppSym)
            value += self.H1(board)

        return value

    def H1(self, board):
        opp_moves = 0
        player_moves = 0

        for row in range(board.rows):
            for col in range(board.cols):
                if (board.is_legal_move(col, row, self.symbol)):
                    player_moves += 1
                if (board.is_legal_move(col, row, self.oppSym)):
                    opp_moves += 1

        return player_moves - opp_moves

    def get_successors(self, board, player_symbol):
        # Write function that takes the current state and generates all successors obtained by legal moves
        # type:(board, player_symbol) -> (list)

        # Check if the current board has successors currently available.
        # If it does not, then we obtain and add those children to the board.
        board.children.clear()

        # We test for a move and see if it's valid or not. If it is, we add it to the successors list.
        # We loop through each row and column and check if we can place a piece in that column/row.
        for row in range(board.rows):
            for col in range(board.cols):
                if (board.is_legal_move(col, row, player_symbol)):
                    successorBoard = board.cloneOBoard()
                    # If it is a legal move, we assign the column and row to the board's
                    # move property.
                    successorBoard.move = (col, row)
                    # Then we play the move and add that new state to current board's children.

                    successorBoard.play_move(col, row, player_symbol)
                    board.children.append(successorBoard)

        return board.children

    def get_move(self, board):
        # Write function that returns a move (column, row) here using minimax
        # type:(board) -> (int, int)
        return self.alphabeta(board)
