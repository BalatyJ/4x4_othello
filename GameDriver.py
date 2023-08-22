from Players import *
import sys
import OthelloBoard
import matplotlib.pyplot as plt


class GameDriver:
    def __init__(self, p1type="human", p2type="alphabeta", num_rows=4, num_cols=4, p1_eval_type=0, p1_prune=False, p2_eval_type=0, p2_prune=False, p1_depth=8, p2_depth=8):
        if p1type.lower() in "human":
            self.p1 = HumanPlayer('X')

        elif p1type.lower() in "alphabeta":
            self.p1 = AlphaBetaPlayer('X', p1_eval_type, p1_prune, p1_depth)

        else:
            print("Invalid player 1 type!")
            exit(-1)

        if p2type.lower() in "human":
            self.p2 = HumanPlayer('O')

        elif p2type.lower() in "alphabeta":
            self.p2 = AlphaBetaPlayer('O', p2_eval_type, p2_prune, p2_depth)

        else:
            print("Invalid player 2 type!")
            exit(-1)

        self.board = OthelloBoard.OthelloBoard(
            num_rows, num_cols, self.p1.symbol, self.p2.symbol)
        self.board.initialize()
        self.p2.get_successors(self.board, self.p2.symbol)

    def display(self):
        print("Player 1 (", self.p1.symbol, ") score: ",
              self.board.count_score(self.p1.symbol))

    def process_move(self, curr_player, opponent):
        invalid_move = True
        while (invalid_move):
            (col, row) = curr_player.get_move(self.board)
            if (not self.board.is_legal_move(col, row, curr_player.symbol)):
                print("Invalid move")
            else:
                print("Move:", [col, row], "\n")
                self.board.play_move(col, row, curr_player.symbol)
                return

    def run(self):
        current = self.p1
        opponent = self.p2
        self.board.display()

        cant_move_counter, toggle = 0, 0

        # main execution of game
        print("Player 1(", self.p1.symbol, ") move:")
        # Get a move, then display it in a while loop
        turn_count = 0
        while True:
            if self.board.has_legal_moves_remaining(current.symbol):
                turn_count += 1
                cant_move_counter = 0
                self.process_move(current, opponent)
                self.board.display()
            else:
                print("Can't move")
                if (cant_move_counter == 1):
                    break
                else:
                    cant_move_counter += 1
            toggle = (toggle + 1) % 2
            if toggle == 0:
                current, opponent = self.p1, self.p2
                print("Player 1(", self.p1.symbol, ") move:")
            else:
                current, opponent = self.p2, self.p1
                print("Player 2(", self.p2.symbol, ") move:")

        # decide win/lose/tie state
        state = self.board.count_score(
            self.p1.symbol) - self.board.count_score(self.p2.symbol)

        game_state = -1
        if (state == 0):
            print("Tie game!!")
            game_state = 0
        elif state > 0:
            print("Player 1 Wins!")
            game_state = 1
        else:
            print("Player 2 Wins!")
            game_state = -1
        print("turn count:", turn_count)
        print("total nodes seen by p1", self.p1.total_nodes_seen)
        print("total nodes seen by p2", self.p2.total_nodes_seen)

        return (self.p1.total_nodes_seen, self.p2.total_nodes_seen), game_state


def main():
    board_size = 4
    final_report1 = {
        0: {
            0: {
                2: 0,
                4: 0,
                6: 0,
                8: 0,
                10: 0,
                12: 0
            },
            1: {
                2: 0,
                4: 0,
                6: 0,
                8: 0,
                10: 0,
                12: 0
            },
        },
        1: {
            0: {
                2: 0,
                4: 0,
                6: 0,
                8: 0,
                10: 0,
                12: 0
            },
            1: {
                2: 0,
                4: 0,
                6: 0,
                8: 0,
                10: 0,
                12: 0
            },
        },
        2: {
            0: {
                2: 0,
                4: 0,
                6: 0,
                8: 0,
                10: 0,
                12: 0
            },
            1: {
                2: 0,
                4: 0,
                6: 0,
                8: 0,
                10: 0,
                12: 0
            },
        }
    }

    final_report2 = {
        0: {
            1: {
                2: (0, 0),
                4: (0, 0),
                6: (0, 0),
                8: (0, 0)
            },
            2: {
                2: (0, 0),
                4: (0, 0),
                6: (0, 0),
                8: (0, 0)
            }
        },
        1: {
            0: {
                2: (0, 0),
                4: (0, 0),
                6: (0, 0),
                8: (0, 0)
            },
            2: {
                2: (0, 0),
                4: (0, 0),
                6: (0, 0),
                8: (0, 0)
            }
        },
        2: {
            0: {
                2: (0, 0),
                4: (0, 0),
                6: (0, 0),
                8: (0, 0)
            },
            1: {
                2: (0, 0),
                4: (0, 0),
                6: (0, 0),
                8: (0, 0)
            }
        }
    }

    # First report is for search vs depth at varying depth levels, pruning,
    # and heuristics measured.
    x_label_depth = [2, 4, 6, 8, 10, 12]
    # All games for Search vs. Depth report.
    # Start with current heuristic.
    for heuristic in range(0, 3):
        # Start with pruning disabled, then enabled.
        for pruning in range(0, 2):
            # Start at depth 2, and increment up until past 12.
            for depth in range(2, 13, 2):
                game = GameDriver("alphabeta", "alphabeta", board_size, board_size, heuristic,
                                  pruning, heuristic, pruning, depth, depth)
                final_report1[heuristic][pruning][depth], *_ = game.run()

        # Generate reports for number of nodes/depth searched to.
    # plotMetrics(x_label_depth, final_report1, "Report 1")

    x_label_depth = [2, 4, 6, 8]
    # All games for Heuristic Quality report.
    for heuristicX in range(0, 3):
        for heuristicO in range(0, 3):
            if (heuristicX != heuristicO):
                # Start at depth 2, and increment up until past 12.
                for depth in range(2, 9, 2):

                    game = GameDriver("alphabeta", "alphabeta", board_size, board_size, heuristicX,
                                      1, heuristicO, 1, depth, depth)
                    *_, final_report2[heuristicX][heuristicO][depth] = game.run()

    # Then we create graphs off of the data.

    # plotMetrics(x_label_depth, final_report2, "Report 2")
    # plt.show()


def plotMetricR2(x_label_depth, report_data, HX, HO, figure, axis):

    barWidth = 0.3

    wins, losses = dataAggregateR2(x_label_depth, report_data, HX, HO)
    x_default = [0, 1, 2, 3]
    x1 = [0, 1, 2, 3]
    for i in range(len(x1)):
        x1[i] = x1[i] - barWidth/2
    x2 = [0, 1, 2, 3]
    for i in range(len(x2)):
        x2[i] = x2[i] + barWidth/2

    axis.bar(x1, wins, barWidth, label="Player 1 Wins")
    axis.bar(x2, losses, barWidth, label="Player 1 Loses")

    axis.set_xlabel('Depth of Games Played')
    axis.set_ylabel('Win/Loss Quantities')
    axis.set_xticks(x_default)
    axis.set_xticklabels(x_label_depth)
    axis.legend()
    axis.set_title(
        f'Win Loss rates for Player 1 (X)\nH{HX} vs Player 2 (O) H{HO}.')


def plotMetricR1(x_label_depth, report_data, H, pruning, figure, axis):

    barWidth = 0.3
    if (pruning == 0):
        title = "Off"
    else:
        title = "On"

    searchnodesP1, searchnodesP2 = dataAggregateR1(
        x_label_depth, report_data[H][pruning])
    x_default = [0, 1, 2, 3, 4, 5]
    x1 = [0, 1, 2, 3, 4, 5]
    for i in range(len(x1)):
        x1[i] = x1[i] - barWidth/2
    x2 = [0, 1, 2, 3, 4, 5]
    for i in range(len(x2)):
        x2[i] = x2[i] + barWidth/2

    axis.bar(x1, searchnodesP1, barWidth, label="Player 1 (X)")
    axis.bar(x2, searchnodesP2, barWidth, label="Player 2 (O)")

    axis.set_xlabel('Search Depth Limit')
    axis.set_ylabel('Search Nodes Generated')
    axis.set_xticks(x_default)
    axis.set_xticklabels(x_label_depth)
    axis.legend()
    axis.set_title(f'Search Nodes Generated for H{H}\nPruning {title}.')


def dataAggregateR2(x_label_depth, report_data, heuristicX, heuristicO):
    wins = []
    losses = []
    for depth in x_label_depth:
        result = report_data[heuristicX][heuristicO][depth]
        if (result == 1):
            wins.append(1)
            losses.append(0)
        elif result == -1:
            wins.append(0)
            losses.append(1)
        else:
            wins.append(0)
            losses.append(0)

    return (wins, losses)


def dataAggregateR1(x_label_depth, report_data,):
    depth_results_p1 = []
    depth_results_p2 = []
    for depth in x_label_depth:
        depth_results_p1.append(
            report_data[depth][0])
        depth_results_p2.append(
            report_data[depth][1])
    return (depth_results_p1, depth_results_p2)


def plotMetrics(x_label_depth, report_data, metric):
    if (metric == "Report 2"):
        for heuristicX in report_data.keys():
            for heuristicO in report_data[heuristicX].keys():
                fig, ax = plt.subplots(figsize=(8, 6))
                plotMetricR2(x_label_depth, report_data,
                             heuristicX, heuristicO, fig, ax)
    elif (metric == "Report 1"):
        # Generate first report for searched nodes.
        for heuristic in report_data.keys():
            for pruning in range(0, 2):
                fig, ax = plt.subplots(figsize=(8, 6))
                # Without pruning.
                plotMetricR1(x_label_depth, report_data,
                             heuristic, pruning, fig, ax)


main()
