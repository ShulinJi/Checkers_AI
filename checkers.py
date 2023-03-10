import argparse
import copy
import sys
import time

cache = {}  # you can use this to implement state caching!

pos_inf = 10000
neg_inf = -10000
depth_limit = 8


class State:
    # This class is used to represent a state.
    # board : a list of lists that represents the 8*8 board
    def __init__(self, board):

        self.board = board
        self.v = 0
        self.width = 8
        self.height = 8

    def display(self):
        for i in self.board:
            for j in i:
                print(j, end="")
            print("")
        print("")

    def evaluate_board(self, player):
        score = 0
        for row in range(self.height):
            for col in range(self.width):
                piece = self.board[row][col]
                if piece == 'r':
                    # red player is maximizing player
                    distance_to_other_end = (self.height - 1 - row) / 7
                    score += 3 + distance_to_other_end
                    if col == 0 or col == self.width - 1:
                        score += 1
                elif piece == 'R':
                    # red player is maximizing player
                    if row == 0 or row == self.height - 1 or col == 0 or col == self.width - 1:
                        score += 4
                    else:
                        score += 5
                elif piece == 'b':
                    # red player is maximizing player
                    distance_to_other_end = row / 7
                    score -= 3 - distance_to_other_end
                    if col == 0 or col == self.width - 1:
                        score -= 1
                elif piece == 'B':
                    # red player is maximizing player
                    if row == 0 or row == self.height - 1 or col == 0 or col == self.width - 1:
                        score -= 4
                    else:
                        score -= 5
        return score

    def __lt__(self, other):
        return self.v < other.v

    def check_endgame(self):
        r_count = 0
        b_count = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 'r':
                    r_count += 1
                elif self.board[i][j] == 'R':
                    r_count += 1
                elif self.board[i][j] == 'b':
                    b_count += 1
                elif self.board[i][j] == 'B':
                    b_count += 1
        if r_count == 0 or b_count == 0:
            return True
        else:
            return False
"""
    def evaluate_board(self, maximizingPlayer):
        score = 0
        for row in range(self.height):
            for col in range(self.width):
                piece = self.board[row][col]
                if piece == 'r':
                    if maximizingPlayer:
                        # red player is maximizing player
                        distance_to_other_end = (self.height - 1 - row) / 7
                        score += 3 + distance_to_other_end
                        if col == 0 or col == self.width - 1:
                            score += 1
                    else:
                        # black player is minimizing player
                        distance_to_other_end = row / 7
                        score -= 3 + distance_to_other_end
                        if col == 0 or col == self.width - 1:
                            score -= 1
                elif piece == 'R':
                    if maximizingPlayer:
                        # red player is maximizing player
                        if row == 0 or row == self.height - 1 or col == 0 or col == self.width - 1:
                            score += 4
                        else:
                            score += 5
                    else:
                        # black player is minimizing player
                        if row == 0 or row == self.height - 1 or col == 0 or col == self.width - 1:
                            score -= 4
                        else:
                            score -= 5
                elif piece == 'b':
                    if maximizingPlayer:
                        # red player is maximizing player
                        distance_to_other_end = row / 7
                        score -= 3 - distance_to_other_end
                        if col == 0 or col == self.width - 1:
                            score -= 1
                    else:
                        # black player is minimizing player
                        distance_to_other_end = (self.height - 1 - row) / 7
                        score += 3 - distance_to_other_end
                        if col == 0 or col == self.width - 1:
                            score += 1
                elif piece == 'B':
                    if maximizingPlayer:
                        # red player is maximizing player
                        if row == 0 or row == self.height - 1 or col == 0 or col == self.width - 1:
                            score -= 4
                        else:
                            score -= 5
                    else:
                        # black player is minimizing player
                        if row == 0 or row == self.height - 1 or col == 0 or col == self.width - 1:
                            score += 4
                        else:
                            score += 5
        return score
"""


def min_value(states, a, b, depth, player):
    if depth == depth_limit or states.check_endgame() is True:
        """
        if states.check_endgame() is True:
            return states, neg_inf
        else:
        """
        return states, states.evaluate_board('r')
    v = pos_inf
    next_moves = find_all_moves(states, player, depth)
    player = get_next_turn(player)
    for i in next_moves:
        better_state = max_value(i, a, b, depth + 1, player)
        if better_state[1] < v:
            states = copy.deepcopy(i)
            v = better_state[1]
        if v <= a:
            states = copy.deepcopy(i)
            return states, v
        b = min(b, v)
    return states, v


def max_value(states, a, b, depth, player):
    if depth == depth_limit or states.check_endgame() is True:
        """
        if states.check_endgame() is True:
            return states, pos_inf
        else:
        """
        return states, states.evaluate_board('r')
    v = neg_inf
    next_moves = find_all_moves(states, player, depth)
    player = get_next_turn(player)
    for i in next_moves:
        better_state = min_value(i, a, b, depth + 1, player)
        if better_state[1] > v:
            states = copy.deepcopy(i)
            v = better_state[1]
        if v >= b:
            return i, v
        a = max(a, v)
    return states, v


def minimax(states, depth, alpha, beta, maximizingPlayer):
    if depth == depth_limit or states.check_endgame():
        if states.check_endgame() and maximizingPlayer:
            return neg_inf * depth, None
        if states.check_endgame() and not maximizingPlayer:
            return pos_inf * depth, None
        return states.evaluate_board(maximizingPlayer), None

    best_move = None
    if maximizingPlayer:
        max_eval = neg_inf
        for move in find_all_moves(states, 'r', depth):
            child_state = move
            eval, _ = minimax(child_state, depth + 1, alpha, beta, False)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = pos_inf
        for move in find_all_moves(states, 'b', depth):
            child_state = move
            eval, _ = minimax(child_state, depth + 1, alpha, beta, True)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move


def find_all_moves(states, player, depth):
    copy_board = copy.deepcopy(states)
    single_moves = next_single_move(copy_board.board, player)
    copy_board = copy.deepcopy(states)
    next_capture = single_capture([copy_board.board], player)
    list_to_check = []
    capture_to_be_king = []
    multi_capture = []
    if len(next_capture[0]) != 0:
        for x in next_capture[0]:
            if x[1] is True:
                # states that terminates because it becomes a king
                # new_state = State(x[0])
                capture_to_be_king.append(x[0])
            else:
                list_to_check.append(x[0])
    if len(list_to_check) != 0:
        multi_capture = multi_captures(list_to_check, player)
    all_captures = []
    all_captures.extend(multi_capture)
    all_captures.extend(capture_to_be_king)
    all_capture_states = []
    if len(all_captures) != 0:
        for y in all_captures:
            all_capture_states.append(State(y))
        next_moves = copy.deepcopy(all_capture_states)
    else:
        next_moves = copy.deepcopy(single_moves)
    if player == 'r':
        for j in next_moves:
            j.v = j.evaluate_board('r')
        next_moves.sort()
        next_moves.reverse()
    if player == 'b':
        for j in next_moves:
            j.v = j.evaluate_board('r')
        next_moves.sort()
    return next_moves


def alpha_beta_search(states, depth, player):
    state_v = max_value(states, neg_inf, pos_inf, depth, player)
    return_state = copy.deepcopy(state_v[0])
    return return_state


def next_single_move(board, player):
    moves = []
    for i in range(8):
        for j in range(8):
            if player == 'r':
                if board[i][j] == 'r' or board[i][j] == 'R':
                    # capture first -> clear the list and only return the situation of capture
                    # second row cannot capture any chips
                    # if any chips reach other end, terminate and make it king
                    # could have multiple choices for multi-jump (or single capture)
                    if i >= 0 and j < 7 and (board[i][j] == 'r' or board[i][j] == 'R'):
                        if board[i][j] == 'r':
                            if board[i - 1][j + 1] == '.':
                                game_board = copy.deepcopy(board)
                                if i - 1 == 0:
                                    # the chip becomes a king
                                    game_board[i - 1][j + 1] = 'R'
                                    game_board[i][j] = '.'
                                else:
                                    game_board[i - 1][j + 1] = 'r'
                                    game_board[i][j] = '.'
                                next_state = State(game_board)
                                moves.append(next_state)
                        if board[i][j] == 'R':
                            if i != 7 and board[i + 1][j + 1] == '.':
                                game_board = copy.deepcopy(board)
                                game_board[i + 1][j + 1] = 'R'
                                game_board[i][j] = '.'
                                next_state = State(game_board)
                                moves.append(next_state)
                            if i != 0 and board[i - 1][j + 1] == '.':
                                game_board = copy.deepcopy(board)
                                game_board[i - 1][j + 1] = 'R'
                                game_board[i][j] = '.'
                                next_state = State(game_board)
                                moves.append(next_state)
                    if i >= 0 and j > 0 and (board[i][j] == 'r' or board[i][j] == 'R'):
                        if board[i][j] == 'r':
                            if board[i - 1][j - 1] == '.':
                                game_board = copy.deepcopy(board)
                                if i - 1 == 0:
                                    # the chip becomes a king
                                    game_board[i - 1][j - 1] = 'R'
                                    game_board[i][j] = '.'
                                else:
                                    game_board[i - 1][j - 1] = 'r'
                                    game_board[i][j] = '.'
                                next_state = State(game_board)
                                moves.append(next_state)
                        if board[i][j] == 'R':
                            if i != 7 and board[i + 1][j - 1] == '.':
                                game_board = copy.deepcopy(board)
                                game_board[i + 1][j - 1] = 'R'
                                game_board[i][j] = '.'
                                next_state = State(game_board)
                                moves.append(next_state)
                            if i != 0 and board[i - 1][j - 1] == '.':
                                game_board = copy.deepcopy(board)
                                game_board[i - 1][j - 1] = 'R'
                                game_board[i][j] = '.'
                                next_state = State(game_board)
                                moves.append(next_state)
            if player == 'b':
                if board[i][j] == 'b' or board[i][j] == 'B':
                    if i <= 7 and j < 7 and (board[i][j] == 'b' or board[i][j] == 'B'):
                        if board[i][j] == 'b':
                            if board[i + 1][j + 1] == '.':
                                game_board = copy.deepcopy(board)
                                if i + 1 == 7:
                                    # the chip becomes a king
                                    game_board[i + 1][j + 1] = 'B'
                                    game_board[i][j] = '.'
                                else:
                                    game_board[i + 1][j + 1] = 'b'
                                    game_board[i][j] = '.'
                                next_state = State(game_board)
                                moves.append(next_state)
                        if board[i][j] == 'B':
                            if i != 7 and board[i + 1][j + 1] == '.':
                                game_board = copy.deepcopy(board)
                                game_board[i + 1][j + 1] = 'B'
                                game_board[i][j] = '.'
                                next_state = State(game_board)
                                moves.append(next_state)
                            if i != 0 and board[i - 1][j + 1] == '.':
                                game_board = copy.deepcopy(board)
                                game_board[i - 1][j + 1] = 'B'
                                game_board[i][j] = '.'
                                next_state = State(game_board)
                                moves.append(next_state)
                    if i <= 7 and j > 0 and (board[i][j] == 'b' or board[i][j] == 'B'):
                        if board[i][j] == 'b':
                            if board[i + 1][j - 1] == '.':
                                game_board = copy.deepcopy(board)
                                if i + 1 == 7:
                                    # the chip becomes a king
                                    game_board[i + 1][j - 1] = 'B'
                                    game_board[i][j] = '.'
                                else:
                                    game_board[i + 1][j - 1] = 'b'
                                    game_board[i][j] = '.'
                                next_state = State(game_board)
                                moves.append(next_state)
                        if board[i][j] == 'B':
                            if i != 7 and board[i + 1][j - 1] == '.':
                                game_board = copy.deepcopy(board)
                                game_board[i + 1][j - 1] = 'B'
                                game_board[i][j] = '.'
                                next_state = State(game_board)
                                moves.append(next_state)
                            if i != 0 and board[i - 1][j - 1] == '.':
                                game_board = copy.deepcopy(board)
                                game_board[i - 1][j - 1] = 'B'
                                game_board[i][j] = '.'
                                next_state = State(game_board)
                                moves.append(next_state)
    return moves


# board is list of [board]
def single_capture(board, player):
    terminated_states = []
    captures = []
    for x in range(len(board)):
        terminated = True
        new_board = board[x]
        for i in range(8):
            for j in range(8):
                if player == 'r' and (new_board[i][j] == 'r' or new_board[i][j] == 'R'):
                    if new_board[i][j] == 'r' and i != 1:
                        if j < 6 and (new_board[i - 1][j + 1] == 'B' or new_board[i - 1][j + 1] == 'b') and \
                                new_board[i - 2][j + 2] == '.':
                            game_board = copy.deepcopy(new_board)
                            game_board[i][j] = '.'
                            game_board[i - 1][j + 1] = '.'
                            if i - 2 == 0:
                                game_board[i - 2][j + 2] = 'R'
                                terminated = False
                                forced_stop = True
                                # next_state = State(game_board)
                                next_tuple = (game_board, forced_stop)
                                captures.append(next_tuple)
                            else:
                                game_board[i - 2][j + 2] = 'r'
                                terminated = False
                                forced_stop = False
                                # next_state = State(game_board)
                                next_tuple = (game_board, forced_stop)
                                captures.append(next_tuple)
                        if j > 1 and (new_board[i - 1][j - 1] == 'B' or new_board[i - 1][j - 1] == 'b') and \
                                new_board[i - 2][j - 2] == '.':
                            game_board = copy.deepcopy(new_board)
                            game_board[i][j] = '.'
                            game_board[i - 1][j - 1] = '.'
                            if i - 2 == 0:
                                game_board[i - 2][j - 2] = 'R'
                                terminated = False
                                forced_stop = True
                                # next_state = State(game_board)
                                next_tuple = (game_board, forced_stop)
                                captures.append(next_tuple)
                            else:
                                game_board[i - 2][j - 2] = 'r'
                                terminated = False
                                forced_stop = False
                                # next_state = State(game_board)
                                next_tuple = (game_board, forced_stop)
                                captures.append(next_tuple)
                    if new_board[i][j] == 'R':
                        game_board = copy.deepcopy(new_board)
                        forced_stop = False
                        if (i <= 5 and j > 1) and (new_board[i + 1][j - 1] == 'B' or new_board[i + 1][j - 1] == 'b') and \
                                new_board[i + 2][
                                    j - 2] == '.':
                            game_board[i][j] = '.'
                            game_board[i + 1][j - 1] = '.'
                            game_board[i + 2][j - 2] = 'R'
                            terminated = False
                            # next_state = State(game_board)
                            next_tuple = (game_board, forced_stop)
                            captures.append(next_tuple)
                        elif (i <= 5 and j < 6) and (
                                new_board[i + 1][j + 1] == 'B' or new_board[i + 1][j + 1] == 'b') and new_board[i + 2][
                            j + 2] == '.':
                            game_board[i][j] = '.'
                            game_board[i + 1][j + 1] = '.'
                            game_board[i + 2][j + 2] = 'R'
                            terminated = False
                            # next_state = State(game_board)
                            next_tuple = (game_board, forced_stop)
                            captures.append(next_tuple)
                        elif (i >= 2 and j > 1) and (
                                new_board[i - 1][j - 1] == 'B' or new_board[i - 1][j - 1] == 'b') and new_board[i - 2][
                            j - 2] == '.':
                            game_board[i][j] = '.'
                            game_board[i - 1][j - 1] = '.'
                            game_board[i - 2][j - 2] = 'R'
                            terminated = False
                            # next_state = State(game_board)
                            next_tuple = (game_board, forced_stop)
                            captures.append(next_tuple)
                        elif (i >= 2 and j < 6) and (
                                new_board[i - 1][j + 1] == 'B' or new_board[i - 1][j + 1] == 'b') and new_board[i - 2][
                            j + 2] == '.':
                            game_board[i][j] = '.'
                            game_board[i - 1][j + 1] = '.'
                            game_board[i - 2][j + 2] = 'R'
                            terminated = False
                            # next_state = State(game_board)
                            next_tuple = (game_board, forced_stop)
                            captures.append(next_tuple)

                if player == 'b' and (new_board[i][j] == 'b' or new_board[i][j] == 'B'):
                    if new_board[i][j] == 'b' and i != 6:
                        if j < 6 and (new_board[i + 1][j + 1] == 'R' or new_board[i + 1][j + 1] == 'r') and \
                                new_board[i + 2][j + 2] == '.':
                            game_board = copy.deepcopy(new_board)
                            game_board[i][j] = '.'
                            game_board[i + 1][j + 1] = '.'
                            if i + 2 == 7:
                                game_board[i + 2][j + 2] = 'B'
                                terminated = False
                                forced_stop = True
                                # next_state = State(game_board)
                                next_tuple = (game_board, forced_stop)
                                captures.append(next_tuple)
                            else:
                                game_board[i + 2][j + 2] = 'b'
                                terminated = False
                                forced_stop = False
                                # next_state = State(game_board)
                                next_tuple = (game_board, forced_stop)
                                captures.append(next_tuple)
                        elif j > 1 and (new_board[i + 1][j - 1] == 'R' or new_board[i + 1][j - 1] == 'r') and \
                                new_board[i + 2][j - 2] == '.':
                            game_board = copy.deepcopy(new_board)
                            game_board[i][j] = '.'
                            game_board[i + 1][j - 1] = '.'
                            if i + 2 == 7:
                                game_board[i - 2][j - 2] = 'B'
                                terminated = False
                                forced_stop = True
                                # next_state = State(game_board)
                                next_tuple = (game_board, forced_stop)
                                captures.append(next_tuple)
                            else:
                                game_board[i + 2][j - 2] = 'b'
                                terminated = False
                                forced_stop = False
                                # next_state = State(game_board)
                                next_tuple = (game_board, forced_stop)
                                captures.append(next_tuple)
                    if new_board[i][j] == 'B':
                        forced_stop = False
                        game_board = copy.deepcopy(new_board)
                        if (i <= 5 and j > 1) and (new_board[i + 1][j - 1] == 'R' or new_board[i + 1][j - 1] == 'r') and \
                                new_board[i + 2][
                                    j - 2] == '.':
                            terminated = False
                            game_board[i][j] = '.'
                            game_board[i + 1][j - 1] = '.'
                            game_board[i + 2][j - 2] = 'B'
                            # next_state = State(game_board)
                            next_tuple = (game_board, forced_stop)
                            captures.append(next_tuple)
                        elif (i <= 5 and j < 6) and (
                                new_board[i + 1][j + 1] == 'R' or new_board[i + 1][j + 1] == 'r') and new_board[i + 2][
                            j + 2] == '.':
                            terminated = False
                            game_board[i][j] = '.'
                            game_board[i + 1][j + 1] = '.'
                            game_board[i + 2][j + 2] = 'B'
                            # next_state = State(game_board)
                            next_tuple = (game_board, forced_stop)
                            captures.append(next_tuple)
                        elif (i >= 2 and j > 1) and (
                                new_board[i - 1][j - 1] == 'R' or new_board[i - 1][j - 1] == 'r') and new_board[i - 2][
                            j - 2] == '.':
                            terminated = False
                            game_board[i][j] = '.'
                            game_board[i - 1][j - 1] = '.'
                            game_board[i - 2][j - 2] = 'B'
                            # next_state = State(game_board)
                            next_tuple = (game_board, forced_stop)
                            captures.append(next_tuple)
                        elif (i >= 2 and j < 6) and (
                                new_board[i - 1][j + 1] == 'R' or new_board[i - 1][j + 1] == 'r') and new_board[i - 2][
                            j + 2] == '.':
                            terminated = False
                            game_board[i][j] = '.'
                            game_board[i - 1][j + 1] = '.'
                            game_board[i - 2][j + 2] = 'B'
                            # next_state = State(game_board)
                            next_tuple = (game_board, forced_stop)
                            captures.append(next_tuple)

        if terminated is True:
            terminated_states.append(x)
    return captures, terminated_states


# get a capture list and check if there are any more captures by calling single capture several times
# single capture returns a tuple of a list of tuples and terminated
def multi_captures(captures, player):
    # Those who got forced_stop = True will be checked in Minmax, add multi-capture to the forced_stop capture to get total possibility of captures
    # Need to recheck the logic of terminated
    # multi_capture stores the board
    # capture is list of (board)
    # have to avoid duplicate
    multi_capture = []
    for next_move in captures:
        # indicator used to break the while loop when a branch reached the end
        input_board = [next_move]
        indicator = True
        while indicator:
            more_jumps = single_capture(input_board, player)
            if len(more_jumps[0]) == 0:
                indicator = False
                multi_capture.extend(input_board)
            else:
                # add the ones who did not find next states,terminated by no further child
                if more_jumps[1]:
                    for i in more_jumps[1]:
                        # record the tuple (captures, terminated_states) that are terminated, but there are still some left
                        # deal with the situation when we can make choices between single jump and another multi-jump
                        # next_move is a list of boards
                        # i is the index stored in the list
                        terminated_child = input_board[i]
                        multi_capture.append(terminated_child)
                # reset the input of single capture and update it
                input_board = []
                # x is the tuple (board, forced_stop)
                temp = copy.deepcopy(more_jumps[0])
                for x in range(len(more_jumps[0])):
                    if more_jumps[0][x][1] is True:
                        # The chips become a king, terminate here
                        temp.remove(more_jumps[0][x])
                        multi_capture.append(more_jumps[0][x][0])
                        if len(temp) == 0:
                            indicator = False
                    else:
                        # not terminated, keep searching for a new state
                        input_board.append(more_jumps[0][x][0])
    return multi_capture


def get_opp_char(player):
    if player in ['b', 'B']:
        return ['r', 'R']
    else:
        return ['b', 'B']


def get_next_turn(curr_turn):
    if curr_turn == 'r':
        return 'b'
    else:
        return 'r'


def read_from_file(filename):
    f = open(filename)
    lines = f.readlines()
    board = [[str(x) for x in l.rstrip()] for l in lines]
    f.close()

    return board


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzles."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    args = parser.parse_args()

    # start_time = time.time()
    initial_board = read_from_file(args.inputfile)

    initial_state = State(initial_board)
    turn = 'r'
    ctr = 0

    sys.stdout = open(args.outputfile, 'w')
    initial_state.display()
    # sys.stdout = sys.__stdout__

    # depth_limit = 7
    first_player = 'r'
    state = initial_state
    while True:
        next_stat = alpha_beta_search(state, 0, first_player)
        next_stat.display()
        if next_stat.check_endgame() is True:
            break
        state = copy.deepcopy(next_stat)
        first_player = get_next_turn(first_player)

    # final_time = time.time()
    # print("total time costs {}".format(final_time-start_time))
