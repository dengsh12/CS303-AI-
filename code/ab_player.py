import numpy as np
import random
import time

MAX_VALUE = 999999
COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0

black_args = {'board_info': [np.array([[92., -12., -12., 92., 92., -12., -12., 92.],
                                       [-12., 112., 120., 116., 116., 120., 112., -12.],
                                       [-12., 120., 92., -104., -104., 92., 120., -12.],
                                       [92., 116., -104., -112., -112., -104., 116., 92.],
                                       [92., 116., -104., -112., -112., -104., 116., 92.],
                                       [-12., 120., 92., -104., -104., 92., 120., -12.],
                                       [-12., 112., 120., 116., 116., 120., 112., -12.],
                                       [92., -12., -12., 92., 92., -12., -12., 92.]]),
                             np.array([[104., 32., 44., 116., 116., 44., 32., 104.],
                                       [32., 112., -48., 100., 100., -48., 112., 32.],
                                       [44., -48., 80., 20., 20., 80., -48., 44.],
                                       [116., 100., 20., -52., -52., 20., 100., 116.],
                                       [116., 100., 20., -52., -52., 20., 100., 116.],
                                       [44., -48., 80., 20., 20., 80., -48., 44.],
                                       [32., 112., -48., 100., 100., -48., 112., 32.],
                                       [104., 32., 44., 116., 116., 44., 32., 104.]])], 'action_info': [52, -40],
              'unstable_info': [36, -124], 'frontier_info': [-32, -16, -80, -68], 'game_goal_coe': -0.78125}

white_args = {'board_info': [np.array([[40., -116., 96., 64., 64., 96., -116., 40.],
                                       [-116., -52., -20., -88., -88., -20., -52., -116.],
                                       [96., -20., 92., -112., -112., 92., -20., 96.],
                                       [64., -88., -112., -88., -88., -112., -88., 64.],
                                       [64., -88., -112., -88., -88., -112., -88., 64.],
                                       [96., -20., 92., -112., -112., 92., -20., 96.],
                                       [-116., -52., -20., -88., -88., -20., -52., -116.],
                                       [40., -116., 96., 64., 64., 96., -116., 40.]]),
                             np.array([[-32., 92., 48., -8., -8., 48., 92., -32.],
                                       [92., 80., -44., 36., 36., -44., 80., 92.],
                                       [48., -44., 100., 8., 8., 100., -44., 48.],
                                       [-8., 36., 8., 68., 68., 8., 36., -8.],
                                       [-8., 36., 8., 68., 68., 8., 36., -8.],
                                       [48., -44., 100., 8., 8., 100., -44., 48.],
                                       [92., 80., -44., 36., 36., -44., 80., 92.],
                                       [-32., 92., 48., -8., -8., 48., 92., -32.]])], 'action_info': [20, 36],
              'unstable_info': [76, -124], 'frontier_info': [-104, -60, -16, -100], 'game_goal_coe': -1.25}


class AI(object):
    __directions = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]

    def __init__(self, board_size, player, time_out):
        self.board_size = board_size
        self.player = player
        self.time_out = time_out
        self.candidate_list = []
        self.tree = alpha_beta_tree(self.player, self.get_board_value, self.get_valid_moves,
                                    self.get_next_board,
                                    self.is_end, time_out)

        if self.player == COLOR_BLACK:
            self.args = black_args
        else:
            self.args = white_args

        self.board_info = self.args['board_info']  # s, e [-32, 31] * 4                     20
        self.action_info = self.args['action_info']  # s, e [-32, 31] * 4                   2
        self.unstable_info = self.args['unstable_info']  # s, e [-32, 31] * 4               2
        self.frontier_info = self.args['frontier_info']  # [-32, 31] * 4                    4

        self.game_goal_coe = self.args['game_goal_coe']  # b for y = -(b+1)x^2 + bx + 1 (-2 < b < 0) [0, 63] / 32 - 2  1

        self.board_slope = (self.board_info[1] - self.board_info[0]) / 60

    def go(self, chessboard):

        start_time = time.time()
        self.candidate_list.clear()
        valid_moves = self.get_valid_moves(chessboard, self.player)
        if len(valid_moves) == 0:
            return
        action = self.tree.get_action(chessboard, start_time)
        self.candidate_list.extend(valid_moves)
        self.candidate_list.append(action)

    def check_in_board(self, x, y):
        return 0 <= x < self.board_size and 0 <= y < self.board_size

    def get_board_info(self, board, player):
        piece_list = {player: [], 0: [], -player: []}
        for x in range(self.board_size):
            for y in range(self.board_size):
                piece_list[board[x][y]].append((x, y))
        return piece_list

    def get_valid_moves(self, board, player):
        piece_list = self.get_board_info(board, player)
        if len(piece_list[player]) < len(piece_list[0]):
            valid_move = self.get_valid_moves_by_base(board, piece_list[player], player)
        else:
            valid_move = self.get_valid_moves_by_space(board, piece_list[0], player)
        return valid_move

    def get_valid_moves_by_base(self, board, base_list, player):
        moves = set()
        [moves.update(self.find_valid_by_base(board, x, y, player)) for x, y in base_list]
        return list(moves)

    def get_valid_moves_by_space(self, board, space_list, player):
        return [(x, y) for (x, y) in space_list if self.check_space_valid(board, x, y, player)]

    def check_space_valid(self, board, x, y, player):
        for dire in AI.__directions:
            tmp_x, tmp_y = x + dire[0], y + dire[1]
            is_valid = False
            while self.check_in_board(tmp_x, tmp_y):
                if board[tmp_x][tmp_y] == 0:
                    break
                elif board[tmp_x][tmp_y] == -player:
                    is_valid = True
                else:
                    if is_valid:
                        return True
                    else:
                        break
                tmp_x += dire[0]
                tmp_y += dire[1]
        return False

    def find_valid_by_base(self, board, x, y, player):
        valid = set()
        for direc in AI.__directions:
            tmp_x, tmp_y = x + direc[0], y + direc[1]
            is_valid = False
            while self.check_in_board(tmp_x, tmp_y):
                if board[tmp_x][tmp_y] == -player:
                    is_valid = True
                elif board[tmp_x][tmp_y] == player:
                    break
                else:  # =0
                    if is_valid:
                        valid.add((tmp_x, tmp_y))
                    break
                tmp_x += direc[0]
                tmp_y += direc[1]
        return valid

    def find_frontier_piece_num(self, board, player):
        frontier_num = {player: 0, -player: 0}
        for i in range(self.board_size):
            for j in range(self.board_size):
                if board[i][j] == 0:
                    continue
                is_frontier = False
                for direc in AI.__directions:
                    if self.check_in_board(i + direc[0], j + direc[1]) and \
                            board[i + direc[0]][j + direc[1]] == 0:
                        is_frontier = True
                        break
                if is_frontier:
                    frontier_num[board[i][j]] += 1
        return frontier_num[player], frontier_num[-player]

    def get_move_reverse_list(self, board, x, y, player):
        reserve_list = []
        for dire in AI.__directions:
            tmp_x, tmp_y = x + dire[0], y + dire[1]
            tmp_list = []
            while self.check_in_board(tmp_x, tmp_y):
                if board[tmp_x][tmp_y] == -player:
                    tmp_list.append((tmp_x, tmp_y))
                elif board[tmp_x][tmp_y] == player:
                    reserve_list.extend(tmp_list)
                    break
                else:
                    break
                tmp_x += dire[0]
                tmp_y += dire[1]
        return reserve_list

    def get_next_board(self, board, x, y, player):
        new_board = board.copy()

        reverse_li = self.get_move_reverse_list(board, x, y, player)
        for x_, y_ in reverse_li:
            new_board[x_][y_] = player
        new_board[x][y] = player
        return new_board

    def get_board_value_black(self, board, cur_player):

        if self.is_end(board):
            board_sum = np.sum(board)
            if board_sum == 0:
                return 0
            winner = COLOR_BLACK if board_sum * COLOR_BLACK < 0 else COLOR_WHITE
            if winner == COLOR_BLACK:
                return MAX_VALUE / 2
            else:
                return -MAX_VALUE / 2

        piece_number = len(np.where(board != 0)[0])
        board_coe = self.board_slope * piece_number + self.board_info[0]
        multi = board_coe * board
        board_score = - np.sum(multi) * COLOR_BLACK

        cur_valid_moves = self.get_valid_moves(board, cur_player)
        action_coe = (self.action_info[1] - self.action_info[0]) / 60 * piece_number + self.action_info[0]
        action_score = len(cur_valid_moves) * action_coe * (1 if cur_player == COLOR_BLACK else -1)

        cur_oppo_unstable = set()
        [cur_oppo_unstable.update(self.get_move_reverse_list(board, move[0], move[1], cur_player)) \
         for move in cur_valid_moves]
        unstable_coe = (self.unstable_info[1] - self.unstable_info[0]) / 60 * piece_number + self.unstable_info[0]
        unstable_coe = len(cur_oppo_unstable) * unstable_coe * (1 if cur_player == COLOR_BLACK else -1)

        black_num, white_num = self.find_frontier_piece_num(board, COLOR_BLACK)
        black_frontier_coe = (self.frontier_info[1] - self.frontier_info[0]) / 60 * piece_number + self.frontier_info[0]
        white_frontier_coe = (self.frontier_info[3] - self.frontier_info[2]) / 60 * piece_number + self.frontier_info[2]
        frontier_num = (black_frontier_coe * black_num - white_frontier_coe * white_num)

        assist_score = board_score + action_score + unstable_coe + frontier_num

        game_goal_score = - np.sum(board) * COLOR_BLACK

        b = self.game_goal_coe  # b for y = -(b+1)x^2 + bx + 1 (-2 < b < 0) [0, 63] / 32 - 2  1
        x = (piece_number - 4) / 60
        assist_score_rate = -(b + 1) * x ** 2 + b * x + 1

        total_score = (assist_score * assist_score_rate) + game_goal_score * (1 - assist_score_rate)
        return total_score

    def get_board_value(self, board, cur_player):
        val = self.get_board_value_black(board, cur_player)
        # print(val)
        return val if self.player == COLOR_BLACK else -val

    def is_end(self, board):
        piece_number = len(np.where(board != 0)[0])
        if piece_number == 64:
            return True
        return len(self.get_valid_moves(board, COLOR_BLACK)) == 0 and len(self.get_valid_moves(board, COLOR_WHITE)) == 0


def board_to_hash_key(board):
    return board.tobytes()


class alpha_beta_tree(object):

    def __init__(self, color, value_function, get_valid_moves, get_next_board, get_is_end, time_out):
        self.color = color

        self.value_function = value_function
        self.get_valid_moves = get_valid_moves
        self.get_next_board = get_next_board
        self.get_is_end = get_is_end

        self.is_end = {}
        self.valid = {}
        self.value = {}
        self.next_board = {}

        self.history_ab = {}
        self.current_ab = {}

        self.time_out = time_out
        self.start_time = 0

    def get_action(self, board, start_time):
        self.start_time = start_time
        piece_num = len(np.where(board != 0)[0])

        if piece_num > 51:
            self.history_ab = self.current_ab
            self.current_ab = {}
            move, val = self.search_to_end(board, self.color, -MAX_VALUE, MAX_VALUE)
            return move

        final_move = None
        for i in range(1, 64):
            self.history_ab = self.current_ab
            self.current_ab = {}
            move, _ = self.search(board, self.color, -MAX_VALUE, MAX_VALUE, i)
            if move is None:
                print(i - 1)
                return final_move
            else:
                final_move = move
        return final_move

    def update_valid(self, board, cur_player, s):
        if s not in self.valid:
            self.valid[s] = self.get_valid_moves(board, cur_player)
        return self.valid[s]

    def update_value(self, board, cur_player, s):
        if s not in self.value:
            self.value[s] = self.value_function(board, cur_player)
        return self.value[s]

    def update_is_end(self, board, cur_player, s):
        if s not in self.valid:
            self.is_end[s] = self.get_is_end(board)
        return self.is_end[s]

    def update_next_board(self, board, cur_player, s, move):
        if (s, move) not in self.next_board:
            self.next_board[(s, move)] = self.get_next_board(board, move[0], move[1], cur_player)
        return self.next_board[(s, move)]

    def check_time(self):
        return time.time() - self.start_time > 0.985 * self.time_out

    def search(self, board, cur_player, a, b, search_level):
        if self.check_time():
            return None, None

        s = (board.tobytes(), cur_player)
        if search_level == 0 or self.update_is_end(board, cur_player, s):
            val = self.update_value(board, cur_player, s)
            self.current_ab[s] = (val, val)
            return None, val
        valid_moves = self.update_valid(board, cur_player, s)
        if len(valid_moves) == 0:
            _, val = self.search(board, -cur_player, a, b, search_level)
            self.current_ab[s] = (val, val)
            return None, val

        best_action = None
        if cur_player == self.color:  # max
            next_boards = [self.next_board[(s, move)] if (s, move) in self.next_board else None for move in valid_moves]
            next_states = [(tmp.tobytes(), -cur_player) if tmp is not None else None for tmp in next_boards]
            pri_values = [self.history_ab[tmp][1] if tmp in self.history_ab else -MAX_VALUE for tmp in next_states]
            max_to_min_idx = np.argsort(-np.array(pri_values))
            for index in max_to_min_idx:
                move = valid_moves[index]
                next_board = self.update_next_board(board, cur_player, s, move)
                _, val = self.search(next_board, -cur_player, a, b, search_level - 1)

                if self.check_time():
                    return None, None

                if val > a:
                    a = val
                    best_action = move
                if a >= b:
                    break
            self.current_ab[s] = a, b
            return best_action, a
        else:
            next_boards = [self.next_board[(s, move)] if (s, move) in self.next_board else None for move in valid_moves]
            next_states = [(tmp.tobytes(), -cur_player) if tmp is not None else None for tmp in next_boards]
            pri_values = [self.history_ab[tmp][1] if tmp in self.history_ab else MAX_VALUE for tmp in next_states]
            min_to_max_idx = np.argsort(pri_values)
            for index in min_to_max_idx:
                move = valid_moves[index]
                next_board = self.update_next_board(board, cur_player, s, move)
                _, val = self.search(next_board, -cur_player, a, b, search_level - 1)

                if self.check_time():
                    return None, None

                if val < b:
                    b = val
                    best_action = move
                if a >= b:
                    break
            self.current_ab[s] = a, b
            return best_action, b

    def search_to_end(self, board, cur_player, a, b):

        s = (board.tobytes(), cur_player)
        if self.update_is_end(board, cur_player, s):
            val = self.update_value(board, cur_player, s)
            self.current_ab[s] = (val, val)
            return None, val
        valid_moves = self.update_valid(board, cur_player, s)
        if len(valid_moves) == 0:
            _, val = self.search_to_end(board, -cur_player, a, b)
            self.current_ab[s] = (val, val)
            return None, val

        best_action = None
        if cur_player == self.color:  # ma
            for move in valid_moves:
                next_board = self.update_next_board(board, cur_player, s, move)
                _, val = self.search_to_end(next_board, -cur_player, a, b)

                if self.check_time():
                    return None, None

                if val > a:
                    a = val
                    best_action = move
                if a >= b:
                    break
            self.current_ab[s] = a, b
            return best_action, a
        else:

            for move in valid_moves:
                next_board = self.update_next_board(board, cur_player, s, move)
                _, val = self.search_to_end(next_board, -cur_player, a, b)

                if self.check_time():
                    return None, None

                if val < b:
                    b = val
                    best_action = move
                if a >= b:
                    break
            self.current_ab[s] = a, b
            return best_action, b

