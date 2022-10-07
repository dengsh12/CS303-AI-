import multiprocessing
from multiprocessing import Pool
import re
import numpy.random

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
        self.history_black_win = 0
        self.history_white_win = 0
        self.live_time = 0
        self.win_num = 0
        self.white_win = 0
        self.black_win = 0
        self.tie_num = 0
        self.score_matrix = [[-1.1 for i in range(8)] for j in range(8)]
        self.score_matrix1 = [[-1.1 for i in range(8)] for j in range(8)]
        self.arb_matrix=[[-1.1 for i in range(8)] for j in range(8)]
        self.arb_matrix1=[[-1.1 for i in range(8)] for j in range(8)]
        # self.delta_matrix= [[-1.1 for i in range(8)] for j in range(8)]
        # score_matrix[0][0]=-30
        # score_matrix[0][7]=-30
        # score_matrix[7][0]=-30
        # score_matrix[7][7]=-30
        # for i in range(4):
        #     ite=order3[i]
        #     score_matrix[ite[0]][ite[1]]=2
        # for i in range(4,16):
        #     ite = order3[i]
        #     score_matrix[ite[0]][ite[1]] = 1
        # for i in range(16,36):
        #     ite = order3[i]
        #     score_matrix[ite[0]][ite[1]]=0
        self.maxD = 3
        # global score_matrix
        self.chessboard_size = chessboard_size
        self.c = 2
        self.t = 2000000
        # score_matrix = [[-(abs(i-4)+abs(j-5)) for i in range(chessboard_size)] for j in range(chessboard_size)]
        # score_matrix[0][0]=-100
        # You are white or black
        self.c1 = 1
        self.c2 = [0 for i in range(3)]
        self.c3 = [0 for i in range(3)]
        self.c4 = [0 for i in range(3)]
        self.color = color
        # the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        # You need add your decision into your candidate_list. System will get the end of your candidate_list as your decision .
        self.candidate_list = []
        self.match = [[{ } for i in range(65)] for j in range(2)]
        # The input is current chessboard.

    def judge_move(self, chessboard: list, turn, loc)  :
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
                        judge = 0
                        p = [i, j]
                        if (found == 1) :
                            break
                        while self.legal(p) :
                            if (judge == 0) :
                                judge = 1
                            elif (judge == 1) :
                                bv = chessboard[p[0]][p[1]]
                                if (bv == -turn) :
                                    judge = 2
                                else :
                                    break
                            elif (judge == 2) :
                                bv = chessboard[p[0]][p[1]]
                                if (bv == turn) :
                                    lis.append((i, j))
                                    found = 1
                                    break
                                elif (bv == 0) :
                                    break
                            p[0] += dir[k][0]
                            p[1] += dir[k][1]

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

    def mct(self, chessboard, turn) :
        random.seed()
        s = 0
        for i in range(8) :
            for j in range(8) :
                if chessboard[i][j] != 0 :
                    s += 1
        times = 1000000
        arrivable = self.get_arrivable(chessboard, self.color)
        if len(arrivable) == 0 :
            return
        ucts = [0 for i in range(len(arrivable))]
        nxt = -turn
        if turn == -1 :
            now = 0
        else :
            now = 1
        if nxt == -1 :
            nxt = 0
        s = 1
        for i in range(8) :
            for j in range(8) :
                if chessboard[i][j] != 0 :
                    s += 1
        nHere = 0
        match = [[] for i in range(len(arrivable))]
        sub_nodes = []
        # random.shuffle(arrivable)
        for idx, ite in enumerate(arrivable) :
            rechange = self.next_board(chessboard, ite, turn)
            chessboard[ite[0]][ite[1]] = turn
            res = self.extend(chessboard, -turn, True)
            match[idx] = [1, res]
            sb = Node()
            sub_nodes.append(sb)
            sb.n = 1
            sb.v = res
            chessboard[ite[0]][ite[1]] = 0
            for ite1 in rechange :
                chessboard[ite1[0]][ite1[1]] = -turn
            nHere += 1
        t1 = time.perf_counter()
        uct1 = [0 for i in range(len(arrivable))]
        for total in range(self.t) :
            # if total%100==0:
            #     print(time.perf_counter())
            #     print(total)
            mv = -10000000
            midx = 0
            for idx, ite in enumerate(arrivable) :
                rechange = self.next_board(chessboard, ite, turn)
                chessboard[ite[0]][ite[1]] = turn
                node = match[idx]
                ucts[idx] = node[1] / node[0] + self.c * ((math.log(nHere) / node[0]) ** 0.5)
                uct1[idx] = node[1] / node[0]
                if mv < ucts[idx] :
                    mv = ucts[idx]
                    midx = idx
                chessboard[ite[0]][ite[1]] = 0
                for ite1 in rechange :
                    chessboard[ite1[0]][ite1[1]] = -turn
            ite = arrivable[midx]
            rechange = self.next_board(chessboard, ite, turn)
            chessboard[ite[0]][ite[1]] = turn
            res = self.sub_mct(chessboard, -turn, True, sub_nodes[midx])
            match[midx][0] += 1
            match[midx][1] += res
            chessboard[ite[0]][ite[1]] = 0
            for ite1 in rechange :
                chessboard[ite1[0]][ite1[1]] = -turn
            nHere += 1
            if time.perf_counter() - t1 > 3.5 :
                break
        midx = 0
        mv = -10000000
        for idx, ite in enumerate(arrivable) :
            v = match[idx][0]
            if mv < v :
                mv = v
                midx = idx
        return arrivable[midx]

    def sub_mct(self, chessboard, turn, lastCan: bool, node: Node) :
        if len(node.arrivable) == 0 :
            node.arrivable = self.get_arrivable(chessboard, turn)
            random.shuffle(node.arrivable)
            arrivable = node.arrivable
        else :
            arrivable = node.arrivable
        ucts = [0 for i in range(len(arrivable))]
        s = 0
        if len(arrivable) == 0 :
            my = 0
            s = 0
            for i in range(8) :
                for j in range(8) :
                    if chessboard[i][j] != 0 :
                        s += 1
                        if chessboard[i][j] == self.color :
                            my += 1
            if s == 64 :
                if my < 32 :
                    return 1
                elif my == 32 :
                    return 0
                else :
                    return -1
            if lastCan :
                if len(node.sub_nodes) == 0 :
                    sb = Node()
                    node.sub_nodes.append(sb)
                    res = self.extend(chessboard, -turn, False)
                    sb.n = 1
                    sb.v = res
                    return res
                else :
                    res = self.sub_mct(chessboard, -turn, False, node.sub_nodes[0])
                    node.n += 1
                    node.v += res
                    return res
            else :
                if my < s / 2 :
                    return 1
                elif my == s / 2 :
                    return 0
                else :
                    return -1
        s = 0
        for i in range(8) :
            for j in range(8) :
                if chessboard[i][j] != 0 :
                    s += 1
        nxt = -turn
        if nxt == -1 :
            nxt = 0
        s += 1
        now = 1 if turn == 1 else 0
        # print(s,flush=True)

        mv = -10000000
        midx = 0
        for idx, ite in enumerate(arrivable) :
            if len(node.sub_nodes) < idx + 1 :
                rechange = self.next_board(chessboard, ite, turn)
                chessboard[ite[0]][ite[1]] = turn
                # node=self.match[nxt][s][tuple(chessboard)]
                # ucts[idx]=node[1]/node[0]+c*cmath.sqrt(cmath.log(nHere)/node[0])
                res = self.extend(chessboard, -turn, True)
                store = Node()
                node.sub_nodes.append(store)
                store.n = 1
                store.v = res
                node.n += 1
                node.v += res
                chessboard[ite[0]][ite[1]] = 0
                for ite1 in rechange :
                    chessboard[ite1[0]][ite1[1]] = -turn
                return res
            else :
                sub = node.sub_nodes[idx]
                if turn != self.color :
                    ucts[idx] = self.c * ((math.log(node.n) / sub.n) ** 0.5) - sub.v / sub.n
                else :
                    ucts[idx] = self.c * ((math.log(node.n) / sub.n) ** 0.5) + sub.v / sub.n
                if mv < ucts[idx] :
                    mv = ucts[idx]
                    midx = idx
        ite = arrivable[midx]
        # print("yes",flush=True)
        rechange = self.next_board(chessboard, ite, turn)
        chessboard[ite[0]][ite[1]] = turn
        res = self.sub_mct(chessboard, -turn, True, node.sub_nodes[midx])
        node.n += 1
        node.v += res
        chessboard[ite[0]][ite[1]] = 0
        for ite1 in rechange :
            chessboard[ite1[0]][ite1[1]] = -turn
        return res

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
        my_num=0
        opp_num=0
        for i in range(8) :
            for j in range(8) :
                s += abs(chessboard[i][j])
                if chessboard[i][j]==self.color:
                    my_num+=1
                elif chessboard[i][j]==-self.color:
                    opp_num+=1
        num=my_num-opp_num

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
        ans = self.c1 * initial + self.c2[k] * stable+self.c3[k]*num+arb+self.c4[k]*front
        return ans

    def extend(self, chessboard: list, turn, lastCan: bool) :
        arrivable = self.get_arrivable(chessboard, turn)
        if len(arrivable) == 0 :
            s = 0
            my = 0
            for i in range(8) :
                for j in range(8) :
                    if chessboard[i][j] != 0 :
                        s += 1
                        if chessboard[i][j] == self.color :
                            my += 1
            if s == 64 :
                if my < 32 :
                    return 1
                elif my == 32 :
                    return 0
                else :
                    return -1
            if lastCan :
                return self.extend(chessboard, -turn, False)
            else :
                if my < s / 2 :
                    return 1
                elif my == s / 2 :
                    return 0
                else :
                    return -1
        selection = random.randint(0, len(arrivable) - 1)
        nxt = arrivable[selection]
        rechange = self.next_board(chessboard, nxt, turn)
        chessboard[nxt[0]][nxt[1]] = turn
        out = self.extend(chessboard, -turn, True)
        chessboard[nxt[0]][nxt[1]] = 0
        for ite in rechange :
            chessboard[ite[0]][ite[1]] = -turn
        return out

    def winner_search(self, board, turnHere, deep, lastCan) :
        maxDepth = 28
        sz = 0
        if ((maxDepth - deep) % 2 == 1) :
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
                if (maxDepth - deep) % 2 == 0 :
                    if nxt == bigInf :
                        if deep == maxDepth :
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
        if deep == maxDepth :
            print(out)
            if bestLocation >= 0 :
                out = order[bestLocation]
            else :
                return -1

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

        if deep == 0 :
            out = self.get_mark(board, turnHere)
            return out
        return out

    def ab_search(self, board, turnHere, deep, alpha, beta, lastCan) :
        if deep == 0 :
            out = self.get_mark(board, turnHere)
            return out
        maxDepth = self.maxD
        sz = 0
        bestLocation = -1
        res = 0
        for idx, ite in enumerate(order2) :
            if self.judge_move(board, turnHere, ite) :
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
                out = order2[bestLocation]
                return out
            else :
                file = open("log.txt", mode="a")
                file.write(str(board))
                file.write('\n')
                file.write(turnHere)
                file.write('\n\n')
                file.flush()
                file.close()
                # print(board)
                # print(turnHere)
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

    def go(self, chessboard) :
        self.candidate_list.clear()
        self.candidate_list = self.get_arrivable(chessboard, self.color)
        s = 0
        # for i in range(8):
        #     for j in range(8):
        #         if chessboard[i][j] != 0:
        #             s += 1
        if (len(self.candidate_list) > 0) :
            self.maxD = 1
            x = self.ab_search(chessboard, self.color, 1, -smallInf, smallInf, True)
            if x == -1 :
                file = open("logwrong.txt", mode="a")
                file.write(str(chessboard))
                file.write('\n')
                file.write(self.color)
                file.write('\n\n')
                file.flush()
                file.close()
                self.candidate_list.append(self.candidate_list[0])
            else :
                self.candidate_list.append(x)


import numpy as np
import random
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)


# don't change the class name
class AI_RANDOM(object) :
    # chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out) :
        global score_matrix
        self.chessboard_size = chessboard_size
        # score_matrix = [[-(abs(i-4)+abs(j-5)) for i in range(chessboard_size)] for j in range(chessboard_size)]
        # score_matrix[0][0]=-100
        # You are white or black
        self.color = color
        # the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        # You need add your decision into your candidate_list. System will get the end of your candidate_list as your decision .
        self.candidate_list = []
        # The input is current chessboard.

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
                        judge = 0
                        p = [i, j]
                        if (found == 1) :
                            break
                        while self.legal(p) :
                            if (judge == 0) :
                                judge = 1
                            elif (judge == 1) :
                                bv = chessboard[p[0]][p[1]]
                                if (bv == -turn) :
                                    judge = 2
                                else :
                                    break
                            elif (judge == 2) :
                                bv = chessboard[p[0]][p[1]]
                                if (bv == turn) :
                                    lis.append((i, j))
                                    found = 1
                                    break
                                elif (bv == 0) :
                                    break
                            p[0] += dir[k][0]
                            p[1] += dir[k][1]

        return lis

    def next_board(self, board: list, point: list, turnHere: int) :
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
        for iHere in range(8) :
            loc[0] = point[0]
            loc[1] = point[1]
            while loc[0] < self.chessboard_size and loc[0] >= 0 and loc[1] < self.chessboard_size and loc[1] > 0 :
                if (board[loc[0]][loc[1]] == turnHere) :
                    while (not (loc[0] == point[0] and loc[1] == point[1])) :
                        nextBoard[loc[0]][loc[1]] = turnHere
                        loc[0] = loc[0] - dir[iHere][0]
                        loc[1] = loc[1] - dir[iHere][1]
                    break
                else :
                    if board[loc[0]][loc[1]] == 0 and (not (loc[0] == point[0] and loc[1] == point[1])) :
                        break
                loc[0] = loc[0] + dir[iHere][0]
                loc[1] = loc[1] + dir[iHere][1]

    def go(self, chessboard) :
        # Clear candidate_list, must do this step
        self.candidate_list.clear()
        # Write your algorithm here
        # Here is the simplest sample:Random decision
        # idx = np.where(chessboard == COLOR_NONE)
        # idx = list(zip(idx[0], idx[1]))
        self.candidate_list = self.get_arrivable(chessboard, self.color)
        l = len(self.candidate_list)
        if (len(self.candidate_list) > 0) :
            self.candidate_list.append(self.candidate_list[random.randint(0, l - 1)])




random_mover = AI_RANDOM(8, COLOR_BLACK, 100)
basicab = AI(8, 0, 100)
# mct = MCT(8, 0, 100)


def playto(black: AI, white: AI) -> int :
    bd = [[0 for i in range(8)] for j in range(8)]
    bd[3][3] = COLOR_WHITE
    bd[3][4] = COLOR_BLACK
    bd[4][3] = COLOR_BLACK
    bd[4][4] = COLOR_WHITE
    black.color=COLOR_BLACK
    white.color=COLOR_WHITE
    # print(len(black.delta_matrix),len(black.delta_matrix[0]))
    for t in range(61) :
        if t % 2 == 0 :
            black.go(bd)
            c = black.candidate_list
            if len(c) > 0 :
                p = c[len(c) - 1]
                black.next_board(bd, p, COLOR_BLACK)
                bd[p[0]][p[1]] = COLOR_BLACK
        else :
            white.go(bd)
            c = white.candidate_list
            if len(c) > 0 :
                p = c[len(c) - 1]
                white.next_board(bd, c[len(c) - 1], COLOR_WHITE)
                bd[p[0]][p[1]] = COLOR_WHITE
    total = 0
    black_num = 0
    for i in range(8) :
        for j in range(8) :
            total += abs(bd[i][j])
            if bd[i][j] == COLOR_BLACK :
                black_num += 1
    if black_num < total / 2 :
        return 1
    elif black_num == total / 2 :
        return 0
    else :
        return -1


def translate(chessboard, loc) :
    x = loc[0]
    y = loc[1]
    chessboard[x][7 - y] = chessboard[7 - x][y] = chessboard[7 - x][7 - y] = chessboard[x][y]

def get_subv(father:int,mother:int,length:int)->int:
    if type(mother)==str:
        print('m')
    here=0
    for i in range(length):
        if random.randint(0,100000)%2==0:
            digit=(father>>i)&1
        else:
            digit=(mother>>i)&1
        here=here|(digit<<i)
        if(random.randint(0,10000)%20==0):
            here=here^(1<<i)
    return here



def product(waiters: list) :
    l = len(waiters)
    for i in range(l) :
        waiter = waiters[i]
        waiter: AI
        mate: AI = waiters[(i + random.randint(0, l - 1)) % l]
        son = AI(8, 0, 100)
        # son.c1 = waiter.c1 if random.randint(0, 100) % 2 == 0 else mate.c1
        # print(waiter.score_matrix[0])
        # print(mate.score_matrix[0])
        # if random.randint(0, 100000) % 12 == 0 :
        #     son.c1 += int(random.randint(-21, 21) / int(total ** 0.25))
        # son.c2 = waiter.c2 if random.randint(0, 100) % 2 == 0 else mate.c2
        # if random.randint(0, 100000) % 12 == 0 :
        #     for j in range(4) :
        #         son.c2[j] += int(random.randint(-21, 21) / int(total ** 0.25))
        # son.c3 = waiter.c3 if random.randint(0, 100) % 2 == 0 else mate.c3
        # if random.randint(0, 100000) % 12 == 0 :
        #     for j in range(4) :
        #         son.c3[j] += int(random.randint(-21, 21) / int(total ** 0.25))

        for row in range(4) :
            for column in range(row + 1) :
                fu = int(waiter.score_matrix[row][column]) + 64
                mu = int(mate.score_matrix[row][column]) + 64
                here = 0
                here=get_subv(fu,mu,7)-64
                son.score_matrix[row][column] = here
                son.score_matrix[column][row] = son.score_matrix[row][column]
                translate(son.score_matrix, [row, column])
                translate(son.score_matrix, [column, row])

                fu = int(waiter.score_matrix1[row][column]) + 64
                mu = int(mate.score_matrix1[row][column]) + 64
                son.score_matrix1[row][column] = get_subv(fu, mu, 7) - 64
                son.score_matrix1[column][row] = son.score_matrix1[row][column]
                translate(son.score_matrix1, [row, column])
                translate(son.score_matrix1, [column, row])

                fu=int(waiter.arb_matrix[row][column])+64
                mu=int(mate.arb_matrix[row][column])+64
                here = get_subv(fu, mu, 7) - 64
                son.arb_matrix[row][column]=here
                son.arb_matrix[column][row]=here
                translate(son.arb_matrix,[row,column])
                translate(son.arb_matrix,[column,row])

                fu=int(waiter.arb_matrix1[row][column])+64
                mu=int(mate.arb_matrix1[row][column])+64
                here = get_subv(fu, mu, 7) - 64
                son.arb_matrix1[row][column]=here
                son.arb_matrix1[column][row]=here
                translate(son.arb_matrix1,[row,column])
                translate(son.arb_matrix1,[column,row])

        son.c2 = [1 for i in range(3)]
        son.c3 = [1 for i in range(3)]
        son.c4= [1 for i in range(3)]
        for i in range(3):
            fu = waiter.c2[i]
            mu = mate.c2[i]
            son.c2[i] = get_subv(fu, mu, 8)
            fu=waiter.c3[i]+64
            mu=mate.c3[i]+64
            son.c3[i]=get_subv(fu,mu,7)-64
            fu=-waiter.c4[i]
            mu=-mate.c4[i]
            son.c4[i]=-get_subv(fu,mu,7)
                    # fu = waiter.c3[i]+32
                    # mu = mate.c3[i]+32
                    # son.c3[i] = get_subv(fu, mu, 6)-32


        waiters.append(son)


def sub_inheritance(waiters: list, start: int, end: int) -> list :
    # print(playNum)
    # l1=[0 for i in range(15)]
    lis = [[0 for i in range(len(waiters))] for j in range(3)]
    l=len(waiters)
    for i in range(start, end) :
        black_player = waiters[i]
        black_player.color = COLOR_BLACK
        for j in range(1, playNum + 1) :
            x: int
            white_player=waiters[(i+j)%l]
            white_player.color = COLOR_WHITE
            res = playto(black_player, white_player)
            if res == 1 :
                lis[0][i] += 1
            elif res == -1 :
                lis[1][(i+j)%l] += 1
            else :
                lis[2][i] += 1
                lis[2][(i+j)%l] += 1
    # print("finish",flush=True)
    return lis

    # print("finish", flush=True)


def sub_inheritance_muti(li) :
    return sub_inheritance(li[0], li[1], li[2])

def play_history(waiters: list,start: int, end: int) -> list :
    # print(playNum)
    # l1=[0 for i in range(15)]
    lis = [[0 for i in range(len(waiters))] for j in range(3)]
    l=len(waiters)
    for i in range(start, end) :
        black_player = waiters[i]
        black_player.color = COLOR_BLACK
        for j in range(1,l) :
            x: int
            white_player=waiters[(i+j)%l]
            white_player.color = COLOR_WHITE
            res = playto(black_player, white_player)
            if res == 1 :
                lis[0][i] += 1
            elif res == -1 :
                lis[1][(i+j)%l] += 1
            else :
                lis[2][i] += 1
                lis[2][(i+j)%l] += 1
    # print("finish",flush=True)
    return lis

    # print("finish", flush=True)


def play_history_multi(li) :
    return play_history(li[0], li[1], li[2])

def now_to_history(waiters: list,history:list,start: int, end: int) -> list :
    # print(playNum)
    # l1=[0 for i in range(15)]
    lis = [[0 for i in range(len(waiters))] for j in range(3)]
    l=len(history)
    for i in range(start, end) :
        black_player = waiters[i]
        black_player.color = COLOR_BLACK
        for j in range(l) :
            x: int
            white_player=history[j]
            white_player.color = COLOR_WHITE
            res = playto(black_player, white_player)
            if res == 1 :
                lis[0][i] += 1
            elif res==0:
                lis[2][i] += 1
        white_player=waiters[i]
        white_player.color=COLOR_WHITE
        for j in range(l) :
            x: int
            black_player=history[j]
            black_player.color = COLOR_BLACK
            res = playto(black_player, white_player)
            if res == -1 :
                lis[1][i] += 1
            elif res==0:
                lis[2][i] += 1
    # print("finish",flush=True)
    return lis

    # print("finish", flush=True)



def now_to_history_muti(li):
    return now_to_history(li[0], li[1], li[2],li[3])


history_winner=[]
history_weight=1
def inheritance(waiters: list) :

    # file1 = open("cores_control.txt", mode="r")
    # s1 = file1.readline()
    # cores = int(s1)
    random.seed()
    random.shuffle(waiters)
    for player in waiters :
        player: AI
        player.win_num = 0
        player.tie_num = 0
        player.black_win = player.white_win = 0
        player.history_black_win=player.history_white_win=0
    length = int(waiter_num / cores)
    args = [[waiters, i * length, (i + 1) * length] for i in range(cores)]

    # res=sub_inheritance_muti(args[0])
    # print(args)
    res=[]
    # file = open("control.txt", mode="r")

    # s = file.readline()
    # if s=="5":
    #     sc_file=open("score.txt",mode="r")
    #     for i in range(8):
    #         s_inner=sc_file.readline()
    #         arr=s_inner.split(',')
    #         for j in range(len(arr)):
    #             basicab.score_matrix[i][j] = int(arr[j])
    #
    #     print(basicab.score_matrix)
    with Pool(cores) as p :
        res = p.map(sub_inheritance_muti, args)
    p.join()
    p.close()
    # print("go", flush=True)
    for idx, lis in enumerate(res) :
        for i in range(waiter_num):
            a = waiters[i]
            a: AI
            a.black_win+=res[idx][0][i]
            a.white_win+=res[idx][1][i]
            a.tie_num+=res[idx][2][i]
    for waiter in waiters:
        waiter:AI
        waiter.win_num=min(waiter.white_win,waiter.black_win)
    # normal_res=
    list.sort(waiters, key=lambda ai : (ai.win_num, ai.tie_num), reverse=True)
    winner:AI=waiters[0]
    history_num=int(cores/3)
    if len(history_winner)<history_num-1:
        cp=AI(8,0,100)
        for i in range(8):
            for j in range(8):
                cp.score_matrix[i][j]=winner.score_matrix[i][j]
                cp.score_matrix1[i][j]=winner.score_matrix1[i][j]
                cp.arb_matrix[i][j]=winner.arb_matrix[i][j]
                cp.arb_matrix1[i][j]=winner.arb_matrix1[i][j]
        cp.c1=winner.c1
        for i in range(3):
            cp.c2[i]=winner.c2[i]
            cp.c3[i]=winner.c3[i]
            cp.c4[i]=winner.c4[i]
        history_winner.append(cp)
    else:
        for history in history_winner:
            history:AI
            history.black_win=history.white_win=history.tie_num=history.history_black_win=history.history_white_win=0

        args = [[waiters, history_winner,i * length, (i + 1) * length] for i in range(cores)]
        with Pool(cores) as p2 :
            res_now_to_history = p2.map(now_to_history_muti, args)
        for idx,lis in enumerate(res_now_to_history):
            for i in range(waiter_num):
                a:AI=waiters[i]
                a.black_win+=res_now_to_history[idx][0][i]*history_weight
                a.white_win+=res_now_to_history[idx][1][i]*history_weight
                a.tie_num+=res_now_to_history[idx][2][i]*history_weight
                a.history_black_win+=res_now_to_history[idx][0][i]*history_weight
                a.history_white_win+=res_now_to_history[idx][1][i]*history_weight
        for wt in waiters:
            wt.win_num=min(wt.black_win,wt.white_win)
        list.sort(waiters, key=lambda ai : (ai.win_num, ai.tie_num), reverse=True)
        winner: AI = waiters[0]

        cp = AI(8, 0, 100)
        for i in range(8) :
            for j in range(8) :
                cp.score_matrix[i][j] = winner.score_matrix[i][j]
                cp.score_matrix1[i][j] = winner.score_matrix1[i][j]
                cp.arb_matrix[i][j]=winner.arb_matrix[i][j]
                cp.arb_matrix1[i][j]=winner.arb_matrix1[i][j]
        cp.c1 = winner.c1
        cp.live_time=total
        for i in range(3) :
            cp.c2[i] = winner.c2[i]
            cp.c3[i] = winner.c3[i]
            cp.c4[i] = winner.c4[i]
        history_winner.append(cp)

        length = 1
        args=[[history_winner,i*length,(i+1)*length] for i in range(history_num)]
        for wt in history_winner:
            wt.win_num=0
            wt.black_win=0
            wt.white_win=0
            wt.tie_num=0
        with Pool(history_num) as p1 :
            res_history = p1.map(play_history_multi, args)
        p1.join()
        p1.close()
        for idx,lis in enumerate(res_history):
            for i in range(history_num):
                a:AI=history_winner[i]
                a.black_win+=res_history[idx][0][i]
                a.white_win+=res_history[idx][1][i]
                a.tie_num+=res_history[idx][2][i]
        for wt in history_winner:
            wt.win_num=min(wt.black_win,wt.white_win)
        list.sort(history_winner,key=lambda ai:(ai.win_num,ai.tie_num),reverse=True)
        history_winner.pop()
    history_out = open("history.txt", mode="w")
    for waiter in waiters:
        waiter:AI
        waiter.win_num=min(waiter.white_win,waiter.black_win)
    for wt in history_winner:
        wt:AI
        history_out.writelines(['life time:' + str(wt.live_time), ',black_wins:' + str(wt.black_win) + ',white_wins:' + str(
            wt.white_win) + ',total_win:' + str(wt.win_num)  +',history_black_win:'+str(wt.history_black_win) +',history_white_win:'+str(wt.history_white_win)+'ties:'+ str(wt.tie_num) + "\n",
                        str(wt.score_matrix) + "\n", str(wt.score_matrix1) + "\n",str(wt.arb_matrix)+"\n",str(wt.arb_matrix1)+"\n",
                        str((str(wt.c1), str(wt.c2), str(wt.c3), str(wt.c4))) + "\n"])
    history_out.flush()
    history_out.close()
    if True:
        out = open("log.txt", mode="w")
        for i in range(int(waiter_num/2)) :
            wt = waiters[i]
            wt:AI
            out.writelines(['life time:'+str(wt.live_time),',black_wins:' + str(wt.black_win) + ',white_wins:' + str(
                wt.white_win) + ',total_win:' + str(wt.win_num)  +',history_black_win:'+str(wt.history_black_win) +',history_white_win:'+str(wt.history_white_win)+ ',ties:' + str(wt.tie_num) + "\n",
                            str(wt.score_matrix) + "\n",str(wt.score_matrix1)+"\n", str(wt.arb_matrix)+"\n",str(wt.arb_matrix1)+"\n",str((str(wt.c1), str(wt.c2), str(wt.c3),str(wt.c4)))+"\n"])
        out.flush()
        out.close()
    # file.close()


    for t in range(int(waiter_num / 2)) :
        waiters.pop()
        waiters[t].live_time+=1
    list.sort(waiters, key=lambda ai : (ai.live_time,ai.win_num, ai.tie_num), reverse=True)
    winner: AI = waiters[0]
    print(f"life time:{winner.live_time},black_win:{winner.black_win},white_win:{winner.white_win},total_win:{winner.win_num},ties:{winner.tie_num},history_black_win:{winner.history_black_win},history_white_win:{winner.history_white_win}")
    print(f"{winner.score_matrix}")
    print(f"{winner.score_matrix1}")
    print(f"{winner.arb_matrix}")
    print(f"{winner.arb_matrix1}")
    print((winner.c1, winner.c2, winner.c3,winner.c4))
    product(waiters)
    # for i in range(int(waiter_num/2)):


total = 1
cores = 30

#
# def read(s:str)->int:
#     for ch in s:
#         if str.isdigit(ch):


if __name__ == "__main__" :
    random.seed()
    # playNum=4
    # waiter_num=180
    basicab.score_matrix = [[1 for i in range(8)] for j in range(8)]
    basicab.score_matrix1 = [[1 for i in range(8)] for j in range(8)]
    basicab.delta_matrix = [[0 for i in range(8)] for j in range(8)]
    basicab.c1 = 1
    basicab.c2 = [0 for i in range(4)]
    basicab.c3 = [0 for i in range(4)]
    basicab.c4 = [0 for i in range(4)]
    waiters = []
    # f=open("log.txt")
    for i in range(int(waiter_num)) :
        here = AI(8, 0, 100)
        waiters.append(here)
    #     f.readline()
    #     s = f.readline()
    #     digits = re.findall(r'-?\d+', s)
    #     for ii in range(8):
    #         for jj in range(8):
    #             here.score_matrix[ii][jj]=int(digits[ii*8+jj])
    #     s = f.readline()
    #     digits = re.findall(r'-?\d+', s)
    #     for ii in range(8):
    #         digits=re.findall(r'-?\d+',s)
    #         for jj in range(8):
    #             here.score_matrix1[ii][jj]=int(digits[ii*8+jj])
    #     s = f.readline()
    #     digits = re.findall(r'-?\d+', s)
    #     for ii in range(8) :
    #         digits = re.findall(r'-?\d+', s)
    #         for jj in range(8) :
    #             here.arb_matrix[ii][jj] =int(digits[ii*8+jj])
    #     s = f.readline()
    #     digits = re.findall(r'-?\d+', s)
    #     for ii in range(8) :
    #         digits = re.findall(r'-?\d+', s)
    #         for jj in range(8) :
    #             here.arb_matrix1[ii][jj] = int(digits[ii*8+jj])
    #     s=f.readline()
    #     digits=re.findall(r'-?\d+',s)
    #     here.c1=1
    #     for ii in range(3):
    #         here.c2[ii]=int(digits[ii+1])
    #     for ii in range(3):
    #         here.c3[ii]=int(digits[ii+4])
    #     for ii in range(3):
    #         here.c4[ii]=int(digits[ii+7])
    # product(waiters)

        for j in range(3) :
            here.c2[j] = 0
            here.c3[j] = random.randint(-64, 63)
            here.c4[j] = random.randint(-127, 0)
        for row in range(4) :
            for column in range(row + 1) :
                v = random.randint(-64, 63)
                v1 = random.randint(-64, 63)
                here.score_matrix[row][column] = v
                here.score_matrix[column][row] = here.score_matrix[row][column]
                here.score_matrix1[row][column] = v1
                here.score_matrix1[column][row] = here.score_matrix1[row][column]
                v = random.randint(-64, 63)
                v1 = random.randint(-64, 63)
                here.arb_matrix[row][column] = v
                here.arb_matrix[column][row] = v
                here.arb_matrix1[row][column] = v1
                here.arb_matrix1[column][row] = v1

                translate(here.score_matrix, [row, column])
                translate(here.score_matrix, [column, row])
                translate(here.score_matrix1, [row, column])
                translate(here.score_matrix1, [column, row])
                translate(here.arb_matrix, [row, column])
                translate(here.arb_matrix, [column, row])
                translate(here.arb_matrix1, [row, column])
                translate(here.arb_matrix1, [column, row])
                # translate(here.delta_matrix, [row, column])
                # translate(here.delta_matrix, [column, row])

        here.c1 = 1
        # here.c2 = [40 + random.randint(-30, 30) for i1 in range(4)]
        # here.c3 = [5 + random.randint(-5, 50) for i1 in range(4)]
    for i in range(5) :
        here = waiters[i]
        v = random.randint(-64, 63)
        v1 = random.randint(-64, 63)
        for row in range(4) :
            for column in range(row + 1) :
                here.score_matrix[row][column] = v
                here.score_matrix[column][row] = here.score_matrix[row][column]
                here.score_matrix1[row][column] = v1
                here.score_matrix1[column][row] = here.score_matrix1[row][column]
                here.arb_matrix[row][column] = 0
                here.arb_matrix[column][row] = 0
                here.arb_matrix1[row][column] = 0
                here.arb_matrix1[column][row] = 0
                # here.delta_matrix[row][column] = random.randint(-100, 100)
                # here.delta_matrix[column][row] = here.delta_matrix[row][column]
                translate(here.score_matrix, [row, column])
                translate(here.score_matrix, [column, row])
                translate(here.score_matrix1, [row, column])
                translate(here.score_matrix1, [column, row])
                translate(here.arb_matrix, [row, column])
                translate(here.arb_matrix, [column, row])
                translate(here.arb_matrix1, [row, column])
                translate(here.arb_matrix1, [column, row])
                # translate(here.delta_matrix, [row, column])
                # translate(here.delta_matrix, [column, row])
        for j in range(3) :
            here.c3[j] = 0
            here.c4[j] = 0
    while True :
        random.seed()
        inheritance(waiters)
        print(f"total:{total}", flush=True)
        total += 1
