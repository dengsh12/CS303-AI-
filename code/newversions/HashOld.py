times = 200
import math
import numpy as np
import random
import time

bigInf = 10000000
smallInf = 10000000
COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed()
playNum = 59
waiter_num = 60

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

dir = [[1, 0],
       [-1, 0],
       [0, 1],
       [0, -1],
       [1, 1],
       [-1, - 1],
       [1, -1],
       [-1, 1]]
corner=((0,0),(0,7),(7,0),(7,7))
corner_neighbor=((0,1),(1,0),(0,6),(1,7),(6,0),(7,1),(6,7),(7,6))

class Node :
    def __init__(self) :
        self.arrivable = []
        self.n = 0
        self.v = 0
        self.sub_nodes = []


class AI(object) :
    # chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out) :
        self.live_time=0
        self.win_num = 0
        self.white_win = 0
        self.black_win = 0
        self.tie_num = 0
        self.TLimit=4.4
        self.score_matrix =  [[52, -41, -32, 62, 62, -32, -41, 52], [-41, 39, 60, 62, 62, 60, 39, -41], [-32, 60, 27, -48, -48, 27, 60, -32],
         [62, 62, -48, -52, -52, -48, 62, 62], [62, 62, -48, -52, -52, -48, 62, 62],
         [-32, 60, 27, -48, -48, 27, 60, -32], [-41, 39, 60, 62, 62, 60, 39, -41], [52, -41, -32, 62, 62, -32, -41, 52]]
        self.score_matrix1 =       [[48, -33, -13, 51, 51, -13, -33, 48], [-33, 58, 54, 20, 20, 54, 58, -33], [-13, 54, 40, -38, -38, 40, 54, -13],
         [51, 20, -38, 44, 44, -38, 20, 51], [51, 20, -38, 44, 44, -38, 20, 51], [-13, 54, 40, -38, -38, 40, 54, -13],
         [-33, 58, 54, 20, 20, 54, 58, -33], [48, -33, -13, 51, 51, -13, -33, 48]]

        self.arb_matrix=      [[-53, 56, 19, -15, -15, 19, 56, -53], [56, -21, -22, 38, 38, -22, -21, 56], [19, -22, 19, 10, 10, 19, -22, 19],
         [-15, 38, 10, -45, -45, 10, 38, -15], [-15, 38, 10, -45, -45, 10, 38, -15], [19, -22, 19, 10, 10, 19, -22, 19],
         [56, -21, -22, 38, 38, -22, -21, 56], [-53, 56, 19, -15, -15, 19, 56, -53]]
        self.arb_matrix1=    [[40, 53, 55, 46, 46, 55, 53, 40], [53, 2, 8, 44, 44, 8, 2, 53], [55, 8, -57, -45, -45, -57, 8, 55],
         [46, 44, -45, -40, -40, -45, 44, 46], [46, 44, -45, -40, -40, -45, 44, 46], [55, 8, -57, -45, -45, -57, 8, 55],
         [53, 2, 8, 44, 44, 8, 2, 53], [40, 53, 55, 46, 46, 55, 53, 40]]



        self.maxD = 3
        self.chessboard_size = 8
        self.c = 2
        self.t = 2000000
        self.c1 = 1
        self.c2 =[221, 201, 226]
        self.c3 = [53, 9, -48]
        self.c4 =[-40, -58, -57]



        self.color = color
        self.time_out = time_out
        # You need add your decision into your candidate_list. System will get the end of your candidate_list as your decision .
        self.candidate_list = []
        self.match = {}
        # The input is current chessboard.

    def judge_move(self, chessboard: list, turn, loc) -> bool :
        if chessboard[loc[0]][loc[1]] != 0 :
            return False
        for k in range(8) :
            judge = 1
            p = [loc[0] + dir[k][0], loc[1] + dir[k][1]]
            while self.legal(p) :
                if (judge == 1) :
                    bv = chessboard[p[0]][p[1]]
                    if (bv == -turn) :
                        judge = 2
                    else :
                        break
                elif (judge == 2) :
                    bv = chessboard[p[0]][p[1]]
                    if (bv == turn) :
                        return True
                    elif (bv == 0) :
                        break
                p[0] += dir[k][0]
                p[1] += dir[k][1]
        return False

    def legal(self, p) :
        if ((p[0] >= 0 and p[0] < self.chessboard_size) and (p[1] >= 0 and p[1] < self.chessboard_size)) :
            return True
        return False

    def get_arrivable(self, chessboard: list, turn) -> list :
        dir = [[1, 0],
               [-1, 0],
               [0, 1],
               [0, -1],
               [1, 1],
               [-1, - 1],
               [1, -1],
               [-1, 1]]
        lis = []
        for i in range(self.chessboard_size) :
            for j in range(self.chessboard_size) :
                if (chessboard[i][j] == 0) :
                    found = 0
                    for k in range(8) :
                        p = [i + dir[k][0], j + dir[k][1]]
                        if self.legal(p) and chessboard[p[0]][p[1]] == -turn :
                            p[0] += dir[k][0]
                            p[1] += dir[k][1]
                            while self.legal(p) :
                                if chessboard[p[0]][p[1]] == turn :
                                    found = 1
                                    break
                                elif chessboard[p[0]][p[1]] == 0 :
                                    break
                                p[0] += dir[k][0]
                                p[1] += dir[k][1]
                        if found == 1 :
                            lis.append((i, j))
                            break
        return lis

    def next_board(self, board: list, point: list, turnHere: int) -> list :
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
        for iHere in range(8) :
            loc[0] = point[0] + dir[iHere][0]
            loc[1] = point[1] + dir[iHere][1]
            while loc[0] < self.chessboard_size and loc[0] >= 0 and loc[1] < self.chessboard_size and loc[1] >= 0 :
                if (board[loc[0]][loc[1]] == turnHere) :
                    while (not (loc[0] == point[0] and loc[1] == point[1])) :
                        nextBoard[loc[0]][loc[1]] = turnHere
                        loc[0] = loc[0] - dir[iHere][0]
                        loc[1] = loc[1] - dir[iHere][1]
                        if not (loc[0] == point[0] and loc[1] == point[1]) :
                            lis.append([loc[0], loc[1]])
                    break
                else :
                    if nextBoard[loc[0]][loc[1]] == 0 :
                        break
                loc[0] = loc[0] + dir[iHere][0]
                loc[1] = loc[1] + dir[iHere][1]
        return lis

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
        arb_my=self.get_arrivable(chessboard,self.color)
        arb_opp=self.get_arrivable(chessboard,-self.color)
        arb=0
        for action in arb_my:
            x=action[0]
            y=action[1]
            if s<=44:
                arb+=self.arb_matrix[x][y]
            else:
                arb+=self.arb_matrix1[x][y]
        for action in arb_opp:
            x = action[0]
            y = action[1]
            if s<=44:
                arb-=self.arb_matrix[x][y]
            else:
                arb-=self.arb_matrix1[x][y]
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
        for i in range(8) :
            for j in range(8) :
                if is_stable[i][j] == 1 :
                    if chessboard[i][j] == self.color :
                        stable -= 1
                    else :
                        stable += 1
        ans = self.c1 * initial + self.c2[k] * stable+arb+self.c4[k]*front
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

    def ab_search(self, board, turnHere, deep, alpha, beta, lastCan, startTime) :
        if (time.time() - startTime > self.TLimit) :
            return -bigInf
        if deep == 0 :
            out = self.get_mark(board, turnHere)
            return out
        maxDepth = self.maxD
        sz = 0
        bestLocation = -1
        res = 0
        lis = [0 for i in range(65)]
        for i in range(8) :
            for j in range(8) :
                lis[i * 8 + j] = board[i][j]
        lis[64] = turnHere
        tp = tuple(lis)
        match = self.match
        if (tp in match) :
            arb = match[tp]
        else :
            arb = self.get_arrivable(board, turnHere)
            match[tp] = arb
        for idx, ite in enumerate(arb) :
            sz = 1
            rechange = self.next_board(board, ite, turnHere)
            board[ite[0]][ite[1]] = turnHere
            nxt = self.ab_search(board, -turnHere, deep - 1, alpha, beta, True, startTime)
            board[ite[0]][ite[1]] = 0
            for ite1 in rechange :
                board[ite1[0]][ite1[1]] = -turnHere
            if nxt == -bigInf :
                return -bigInf
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
        if (time.time() - startTime > self.TLimit) :
            return -bigInf
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
                    return self.ab_search(board, -turnHere, deep - 1, alpha, beta, False, startTime)
                else :
                    return self.get_mark(board, turnHere)
        return alpha if (maxDepth - deep) % 2 == 0 else beta

    def go(self, chessboard) :
        self.candidate_list.clear()
        self.candidate_list = self.get_arrivable(chessboard, self.color)
        s = 0
        for i in range(8) :
            for j in range(8) :
                if chessboard[i][j] != 0 :
                    s += 1
        if (len(self.candidate_list) > 0) :
            # self.maxD = 1
            # self.candidate_list.append(self.ab_search(chessboard, self.color, 1, -smallInf, smallInf, True))
            if s >= 55 :
                self.maxD = 3
                move = self.winner_search(chessboard, self.color, self.maxD, True)
                if move == -1 :
                    self.maxD = 3
                    self.candidate_list.append(
                        self.ab_search(chessboard, self.color, 3, -smallInf, smallInf, True, time.time()))
                else :
                    self.candidate_list.append(move)
                # self.candidate_list.append(self.winner_search(chessboard, self.color, 28, True))
            else :
                t = time.time()
                d = 3
                self.maxD = 3
                res = self.ab_search(chessboard, self.color, d, -smallInf, smallInf, True, t)
                while res != -bigInf :
                    self.candidate_list.append(res)
                    d += 1
                    self.maxD = d
                    res = self.ab_search(chessboard, self.color, d, -smallInf, smallInf, True, t)
                    if d>=8:
                        break

