times = 200
import math
import numpy as np
import random
import time

bigInf = 10000000
smallInf = 100000000
COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed()

order = (
(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6),
(7, 7),
(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7),
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6),
(2, 1), (3, 1), (4, 1), (5, 1), (2, 6), (3, 6), (4, 6), (5, 6),
(2, 2), (2, 3), (2, 4), (2, 5), (5, 2), (5, 3), (5, 4), (5, 5),
(3, 2), (4, 2), (3, 5), (4, 5),
(3, 3), (3, 4), (4, 3), (4, 4),
)

order2 = (
    (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6),
    (2, 1), (3, 1), (4, 1), (5, 1), (2, 6), (3, 6), (4, 6), (5, 6),
    (2, 2), (2, 3), (2, 4), (2, 5), (5, 2), (5, 3), (5, 4), (5, 5),
    (3, 2), (4, 2), (3, 5), (4, 5),
    (3, 3), (3, 4), (4, 3), (4, 4),
    (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5),
    (7, 6), (7, 7),
    (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7),
)

order3 = (
    (3, 3), (3, 4), (4, 3), (4, 4),

    (3, 2), (4, 2), (3, 5), (4, 5),
    (2, 2), (2, 3), (2, 4), (2, 5), (5, 2), (5, 3), (5, 4), (5, 5),

    (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6),
    (2, 1), (3, 1), (4, 1), (5, 1), (2, 6), (3, 6), (4, 6), (5, 6),

    (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5),
    (7, 6), (7, 7),
    (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7),
)

order4 = (
    (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7),
    (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)
)

order5 = (
    (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
    (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)
)

corner=((0,0),(0,7),(7,0),(7,7))
corner_neighbor=((0,1),(1,0),(0,6),(1,7),(6,0),(7,1),(6,7),(7,6))
dir = [[1, 0],
       [-1, 0],
       [0, 1],
       [0, -1],
       [1, 1],
       [-1, - 1],
       [1, -1],
       [-1, 1]]


class Node:
    def __init__(self):
        self.arrivable = []
        self.n = 0
        self.v = 0
        self.sub_nodes = []


class AI(object):

    # chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.score_matrix =      [[38, -7, 3, 30, 30, 3, -7, 38], [-7, 56, 25, 41, 41, 25, 56, -7], [3, 25, 7, -3, -3, 7, 25, 3],
         [30, 41, -3, -8, -8, -3, 41, 30], [30, 41, -3, -8, -8, -3, 41, 30], [3, 25, 7, -3, -3, 7, 25, 3],
         [-7, 56, 25, 41, 41, 25, 56, -7], [38, -7, 3, 30, 30, 3, -7, 38]]
        self.score_matrix1 =   [[21, -62, 48, 40, 40, 48, -62, 21], [-62, 59, 52, 5, 5, 52, 59, -62], [48, 52, 43, -8, -8, 43, 52, 48],
         [40, 5, -8, 29, 29, -8, 5, 40], [40, 5, -8, 29, 29, -8, 5, 40], [48, 52, 43, -8, -8, 43, 52, 48],
         [-62, 59, 52, 5, 5, 52, 59, -62], [21, -62, 48, 40, 40, 48, -62, 21]]

        self.c1 = 1
        self.c2 = [106, 220, 205]
        self.c3 =[-5, 7, 15]
        self.c4=[3, 1, 99]
        self.c5=[-32, -45, -23]




        # ('1', '', '', '', '')

        self.maxD = 3
        # global score_matrix
        self.chessboard_size = chessboard_size

        self.t = 2000000
        # score_matrix = [[-(abs(i-4)+abs(j-5)) for i in range(chessboard_size)] for j in range(chessboard_size)]
        # score_matrix[0][0]=-100
        # You are white or black

        self.color = color
        # the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        # You need add your decision into your candidate_list. System will get the end of your candidate_list as your decision .
        self.candidate_list = []
        self.match = [[{ } for i in range(65)] for j in range(2)]
        # The input is current chessboard.

    def judge_move(self, chessboard: list, turn, loc) -> bool:
        if chessboard[loc[0]][loc[1]] != 0:
            return False
        for k in range(8):
            judge = 1
            p = [loc[0] + dir[k][0], loc[1] + dir[k][1]]
            while self.legal(p):
                if (judge == 1):
                    bv = chessboard[p[0]][p[1]]
                    if (bv == -turn):
                        judge = 2
                    else:
                        break
                elif (judge == 2):
                    bv = chessboard[p[0]][p[1]]
                    if (bv == turn):
                        return True
                    elif (bv == 0):
                        break
                p[0] += dir[k][0]
                p[1] += dir[k][1]
        return False

    def legal(self, p):
        if ((p[0] >= 0 and p[0] < self.chessboard_size) and (p[1] >= 0 and p[1] < self.chessboard_size)):
            return True
        return False

    def get_arrivable(self, chessboard: list, turn) -> list:
        dir = [[1, 0],
               [-1, 0],
               [0, 1],
               [0, -1],
               [1, 1],
               [-1, - 1],
               [1, -1],
               [-1, 1]]
        lis = []
        for i in range(self.chessboard_size):
            for j in range(self.chessboard_size):
                if (chessboard[i][j] == 0):
                    found = 0
                    for k in range(8):
                        p = [i+dir[k][0], j+dir[k][1]]
                        if self.legal(p) and chessboard[p[0]][p[1]]==-turn:
                            p[0]+=dir[k][0]
                            p[1]+=dir[k][1]
                            while self.legal(p):
                                if chessboard[p[0]][p[1]]==turn:
                                    found=1
                                    break
                        if found==1:
                            lis.append((i,j))
                            break
        return lis

    def next_board(self, board: list, point: list, turnHere: int) -> list:
        dir = [[1, 0],
               [-1, 0],
               [0, 1],
               [0, -1],
               [1, 1],
               [-1, - 1],
               [1, -1],
               [-1, 1]]
        nextBoard = board
        loc = [0, 0]
        lis = []
        for iHere in range(8):
            loc[0] = point[0] + dir[iHere][0]
            loc[1] = point[1] + dir[iHere][1]
            while loc[0] < self.chessboard_size and loc[0] >= 0 and loc[1] < self.chessboard_size and loc[1] >= 0:
                if (board[loc[0]][loc[1]] == turnHere):
                    while (not (loc[0] == point[0] and loc[1] == point[1])):
                        nextBoard[loc[0]][loc[1]] = turnHere
                        loc[0] = loc[0] - dir[iHere][0]
                        loc[1] = loc[1] - dir[iHere][1]
                        if not (loc[0] == point[0] and loc[1] == point[1]):
                            lis.append([loc[0], loc[1]])
                    break
                else:
                    if nextBoard[loc[0]][loc[1]] == 0:
                        break
                loc[0] = loc[0] + dir[iHere][0]
                loc[1] = loc[1] + dir[iHere][1]
        return lis

    def onemove_eat(self, chessboard: list) -> list :
        res = [[0 for i in range(8)] for j in range(8)]
        for i in range(8) :
            for j in range(8) :
                if chessboard[i][j] == 0 :
                    for k in range(8) :
                        direction = dir[k]
                        loc = [i + direction[0], j + direction[1]]
                        if not self.legal(loc) :
                            continue
                        color = chessboard[loc[0]][loc[1]]
                        if color == 0 :
                            continue
                        loc[0] += direction[0]
                        loc[1] += direction[1]
                        while self.legal(loc) :
                            if chessboard[loc[0]][loc[1]] == -color :
                                loc[0] -= direction[0]
                                loc[1] -= direction[1]
                                while loc != [i, j] :
                                    res[loc[0]][loc[1]] = 1
                                    loc[0] -= direction[0]
                                    loc[1] -= direction[1]
                                break
                            elif chessboard[loc[0]][loc[1]] == 0 :
                                break
                            loc[0] += direction[0]
                            loc[1] += direction[1]

        return res

    def get_mark(self, chessboard: list, nowTurn) :
        ans = 0
        initial = 0
        stable = 0
        is_stable = [[0 for i in range(8)] for j in range(8)]
        s = 0
        # left up
        if chessboard[0][0] != 0 :
            color = chessboard[0][0]
            height = 0
            for i in range(8) :
                if chessboard[0][i] == color :
                    height = i
                    is_stable[0][i] = 1
                else :
                    break
            for i in range(1, 8) :
                j = 0
                if chessboard[i][0] != color :
                    break
                while j < height :
                    if chessboard[i][j] == color :
                        is_stable[i][j] = 1
                    else :
                        break
                    j += 1
                height = j - 1
                if height == 0 :
                    height = 1
            height = 0
            for i in range(8) :
                if chessboard[i][0] == color :
                    height = i
                    is_stable[i][0] = 1
                else :
                    break
            for i in range(1, 8) :
                if chessboard[0][i] != color :
                    break
                j = 0
                while j < height :
                    if chessboard[j][i] == color :
                        is_stable[j][i] = 1
                    else :
                        break
                    j += 1
                height = j - 1
                if height == 0 :
                    height = 1

        # left down
        if chessboard[7][0] != 0 :
            color = chessboard[7][0]
            height: int = 0
            for i in range(8) :
                if chessboard[7][i] == color :
                    height = i
                    is_stable[7][i] = 1
                else :
                    break
            i = 6
            while i >= 0 :
                j = 0
                if chessboard[i][0] != color :
                    break
                while j < height :
                    if chessboard[i][j] == color :
                        is_stable[i][j] = 1
                    else :
                        break
                    j += 1
                height = j - 1
                if height == 0 :
                    height = 1
                i -= 1
            i = 7
            height = 7
            while i >= 0 :
                if chessboard[i][0] == color :
                    is_stable[i][0] = 1
                    height = i
                else :
                    break
                i -= 1
            i = 1
            while i <= 7 :
                if chessboard[7][i] != color :
                    break
                j = 7
                while j > height :
                    if chessboard[j][i] == color :
                        is_stable[j][i] = 1
                    else :
                        break
                    j -= 1
                height = j + 1
                if height == 8 :
                    height = 7
                i += 1

        # right up
        if chessboard[0][7] != 0 :
            color = chessboard[0][7]
            height = 0
            # to left
            for i in range(8) :
                if chessboard[i][7] == color :
                    is_stable[i][7] = 1
                    height = i
                else :
                    break
            i = 6
            while i >= 0 :
                if chessboard[0][i] != color :
                    break
                j = 0
                while j < height :
                    if chessboard[j][i] == color :
                        is_stable[j][i] = 1
                    else :
                        break
                    j += 1
                height = j - 1
                if height == 0 :
                    height = 1
                i -= 1
            # to down
            height = 0
            i = 7
            while i >= 0 :
                if chessboard[0][i] == color :
                    height = i
                    is_stable[0][i] = 1
                else :
                    break
                i -= 1
            for i in range(1, 8) :
                if chessboard[i][7] != color :
                    break
                j = 7
                while j > height :
                    if chessboard[i][j] == color :
                        is_stable[i][j] = 1
                    else :
                        break
                    j -= 1
                height = j + 1
                if height == 7 :
                    height = 6
        # right down
        if chessboard[7][7] != 0 :
            color = chessboard[7][7]
            height = 0
            # to left
            i = 7
            while i >= 0 :
                if chessboard[i][7] == color :
                    is_stable[i][7] = 1
                    height = i
                else :
                    break
                i -= 1

            i = 6
            while i >= 0 :
                if chessboard[0][i] != color :
                    break
                j = 7
                while j > height :
                    if chessboard[j][i] == color :
                        is_stable[j][i] = 1
                    else :
                        break
                    j -= 1
                height = j + 1
                if height == 7 :
                    height = 6
                i -= 1
                # to up
            i = 7
            while i >= 0 :
                if chessboard[7][i] == color :
                    is_stable[7][i] = 1
                    height = i
                else :
                    break
                i -= 1

            i = 6
            while i >= 0 :
                if chessboard[i][7] != color :
                    break
                j = 7
                while j > height :
                    if chessboard[i][j] == color :
                        is_stable[i][j] = 1
                    else :
                        break
                    j -= 1
                i -= 1
                height = j + 1
                if height == 7 :
                    height = 6

        for i in range(8) :
            for j in range(8) :
                s += abs(chessboard[i][j])
        k = int((s - 5) / 20)
        for i in range(8) :
            for j in range(8) :
                if chessboard[i][j] == self.color :
                    # kk=(1-self.score_matrix[i][j])/60
                    if s <= 44 :
                        initial -= self.score_matrix[i][j]
                    else :
                        initial -= self.score_matrix1[i][j]
                elif chessboard[i][j] == -self.color :
                    # kk = (1 - self.score_matrix[i][j]) / 60
                    if s <= 44 :
                        initial += self.score_matrix[i][j]
                    else :
                        initial += self.score_matrix1[i][j]
        for i in range(8) :
            for j in range(8) :
                if is_stable[i][j] == 1 :
                    if chessboard[i][j] == self.color :
                        stable -= 1
                    else :
                        stable += 1
        one_eat = self.onemove_eat(chessboard)
        eat = 0
        for i in range(8) :
            for j in range(8) :
                if one_eat[i][j] == 1 :
                    if chessboard[i][j] == self.color :
                        eat += 1
                    else :
                        eat -= 1
        arb_my = len(self.get_arrivable(chessboard, self.color))
        arb_opp = len(self.get_arrivable(chessboard, -self.color))
        arb = arb_my - arb_opp
        front_self = 0
        front_opp = 0
        for i in range(8) :
            for j in range(8) :
                if chessboard[i][j] != 0 and is_stable[i][j] == 0 :
                    for kk in range(8) :
                        x = i + dir[kk][0]
                        y = j + dir[kk][1]
                        if self.legal((x, y)) :
                            if chessboard[x][y] == 0 :
                                if chessboard[i][j] == self.color :
                                    front_self += 1
                                else :
                                    front_opp += 1
                                break
        front = front_self - front_opp
        if s >= 25 :
            ans = self.c1 * initial + self.c2[k] * stable + self.c3[k] * eat + self.c4[k] * arb + self.c5[k] * front
        else :
            ans = self.c1 * initial + self.c2[k] * stable + self.c4[k] * arb + self.c5[k] * front
        return ans

    def winner_search(self, board, turnHere, deep, lastCan) :
        sz = 0
        if (turnHere != self.color) :
            out = bigInf
        else :
            out = -bigInf
        bestLocation = -1
        res = 0
        for idx, ite in enumerate(order) :
            if self.judge_move(board, turnHere, ite) :
                sz = 1
                rechange = self.next_board(board, ite, turnHere)
                board[ite[0]][ite[1]] = turnHere
                nxt = self.winner_search(board, -turnHere, deep - 1, True)
                board[ite[0]][ite[1]] = 0
                for ite1 in rechange :
                    board[ite1[0]][ite1[1]] = -turnHere
                if turnHere == self.color :
                    if nxt == bigInf :
                        if deep == self.maxD :
                            out = bigInf
                            bestLocation = idx
                            break
                        else :
                            return bigInf
                    elif nxt == 0 :
                        out = 0
                        bestLocation = idx
                else :
                    if nxt == -bigInf :
                        return -bigInf
                    elif nxt == 0 :
                        out = 0
        if deep == self.maxD :
            if self.color == COLOR_BLACK :
                print(out)
            if bestLocation >= 0 :
                out = order[bestLocation]
            else :
                return -1
        if (sz == 0) :
            if deep == self.maxD :
                out = []
                return out
            sc = 0
            my = 0
            for i in range(self.chessboard_size) :
                for j in range(self.chessboard_size) :
                    sc += abs(board[i][j])
                    if board[i][j] == self.color :
                        my += 1
            if sc == 64 :
                if my < sc / 2 :
                    return bigInf
                elif my == sc / 2 :
                    return 0
                else :
                    return -bigInf
            else :
                if lastCan :
                    return self.winner_search(board, -turnHere, deep - 1, False)
                else :
                    if my < sc / 2 :
                        return bigInf
                    elif my == sc / 2 :
                        return 0
                    else :
                        return -bigInf
        return out

    def ab_search(self, board, turnHere, deep, alpha, beta, lastCan) :
        sc = self.get_mark(board, turnHere)
        if deep == 0 :
            out = self.get_mark(board, turnHere)
            return out
        maxDepth = self.maxD
        sz = 0
        bestLocation = -1
        res = 0
        arb = self.get_arrivable(board, turnHere)
        for idx, ite in enumerate(arb) :
            sz = 1
            rechange = self.next_board(board, ite, turnHere)
            board[ite[0]][ite[1]] = turnHere
            nxt = self.ab_search(board, -turnHere, deep - 1, alpha, beta, True)
            board[ite[0]][ite[1]] = 0
            for ite1 in rechange :
                board[ite1[0]][ite1[1]] = -turnHere
            if (maxDepth - deep) % 2 == 0 :
                if alpha < nxt :
                    alpha = nxt
                    bestLocation = idx

                if alpha >= beta :
                    if maxDepth == deep :
                        break
                    return alpha
            else :
                if beta > nxt :
                    beta = nxt
                if alpha >= beta :
                    return beta
        if deep == maxDepth :
            if bestLocation >= 0 :
                out = arb[bestLocation]
                return out
        if (sz == 0) :
            if deep == maxDepth :
                out = []
                return out
            sc = 0
            my = 0
            for i in range(self.chessboard_size) :
                for j in range(self.chessboard_size) :
                    sc += abs(board[i][j])
                    if board[i][j] == self.color :
                        my += 1
            if sc == 64 :
                return self.get_mark(board, turnHere)
            else :
                if lastCan :
                    return self.ab_search(board, -turnHere, deep - 1, alpha, beta, False)
                else :
                    return self.get_mark(board, turnHere)
        return alpha if (maxDepth - deep) % 2 == 0 else beta

    def go(self, chessboard):
        self.candidate_list.clear()
        self.candidate_list = self.get_arrivable(chessboard, self.color)
        s = 0
        for i in range(8):
            for j in range(8):
                if chessboard[i][j] != 0:
                    s += 1
        if (len(self.candidate_list) > 0):
            # self.maxD = 1
            # self.candidate_list.append(self.ab_search(chessboard, self.color, 1, -smallInf, smallInf, True))
            if s >= 55:
                self.maxD=3
                move = self.winner_search(chessboard,self.color,self.maxD,True)
                if move == -1:
                    self.maxD = 3
                    self.candidate_list.append(self.ab_search(chessboard, self.color, 3, -smallInf, smallInf, True))
                else:
                    self.candidate_list.append(move)
                # self.candidate_list.append(self.winner_search(chessboard, self.color, 28, True))
            else:
                t = time.perf_counter()
                self.maxD = 3
                self.candidate_list.append(self.ab_search(chessboard, self.color, 3, -smallInf, smallInf, True))
                if (time.perf_counter()-t<0.65):
                    self.maxD=4
                    self.candidate_list.append(self.ab_search(chessboard, self.color, 4, -smallInf, smallInf, True))
                    if time.perf_counter()-t<0.65:
                        self.maxD = 5
                        self.candidate_list.append(self.ab_search(chessboard, self.color, 5, -smallInf, smallInf, True))
                        if time.perf_counter() - t < 0.65:
                            self.maxD = 6
                            self.candidate_list.append(self.ab_search(chessboard, self.color, 6, -smallInf, smallInf, True))
                print(self.maxD)


