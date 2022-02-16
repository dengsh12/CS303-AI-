import numpy.random

times=200
import math
import numpy as np
import random
import time
bigInf=10000000
smallInf=100000
COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed()
playNum = 30
waiter_num = 20

order = ((0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(7,0),(7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,7),
(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),
(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(6,1),(6,2),(6,3),(6,4),(6,5),(6,6),
(2,1),(3,1),(4,1),(5,1),(2,6),(3,6),(4,6),(5,6),
(2,2),(2,3),(2,4),(2,5),(5,2),(5,3),(5,4),(5,5),
(3,2),(4,2),(3,5),(4,5),
(3,3),(3,4),(4,3),(4,4),
)

order2 = (
(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(6,1),(6,2),(6,3),(6,4),(6,5),(6,6),
(2,1),(3,1),(4,1),(5,1),(2,6),(3,6),(4,6),(5,6),
(2,2),(2,3),(2,4),(2,5),(5,2),(5,3),(5,4),(5,5),
(3,2),(4,2),(3,5),(4,5),
(3,3),(3,4),(4,3),(4,4),
(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(7,0),(7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,7),
(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),
)

order3= (
(3,3),(3,4),(4,3),(4,4),

(3,2),(4,2),(3,5),(4,5),
(2,2),(2,3),(2,4),(2,5),(5,2),(5,3),(5,4),(5,5),

(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(6,1),(6,2),(6,3),(6,4),(6,5),(6,6),
(2,1),(3,1),(4,1),(5,1),(2,6),(3,6),(4,6),(5,6),


(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(7,0),(7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,7),
(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),
)


order4=(
(7,0),(7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,7),
(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0)
)

order5=(
(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),
(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0)
)


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
    score_matrix = [[-1.1 for i in range(8)] for j in range(8)]
    # chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.win_num=0
        self.tie_num=0
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
        self.c1=1
        self.c2=30
        self.c3=5
        self.color = color
        # the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        # You need add your decision into your candidate_list. System will get the end of your candidate_list as your decision .
        self.candidate_list = []
        self.match = [[{} for i in range(65)] for j in range(2)]
        # The input is current chessboard.
    def judge_move(self,chessboard:list,turn,loc)->bool:
        if chessboard[loc[0]][loc[1]]!=0:
            return False
        for k in range(8):
            judge = 1
            p = [loc[0]+dir[k][0], loc[1]+dir[k][1]]
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
                        judge = 0
                        p = [i, j]
                        if (found == 1):
                            break
                        while self.legal(p):
                            if (judge == 0):
                                judge = 1
                            elif (judge == 1):
                                bv = chessboard[p[0]][p[1]]
                                if (bv == -turn):
                                    judge = 2
                                else:
                                    break
                            elif (judge == 2):
                                bv = chessboard[p[0]][p[1]]
                                if (bv == turn):
                                    lis.append((i, j))
                                    found = 1
                                    break
                                elif (bv == 0):
                                    break
                            p[0] += dir[k][0]
                            p[1] += dir[k][1]

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
            while loc[0] < self.chessboard_size and loc[0] >= 0 and loc[1] < self.chessboard_size and loc[1] > 0:
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

    def mct(self, chessboard, turn):
        random.seed()
        s = 0
        for i in range(8):
            for j in range(8):
                if chessboard[i][j] != 0:
                    s += 1
        times = 1000000
        arrivable = self.get_arrivable(chessboard, self.color)
        if len(arrivable) == 0:
            return
        ucts = [0 for i in range(len(arrivable))]
        nxt = -turn
        if turn == -1:
            now = 0
        else:
            now = 1
        if nxt == -1:
            nxt = 0
        s = 1
        for i in range(8):
            for j in range(8):
                if chessboard[i][j] != 0:
                    s += 1
        nHere = 0
        match = [[] for i in range(len(arrivable))]
        sub_nodes = []
        # random.shuffle(arrivable)
        for idx, ite in enumerate(arrivable):
            rechange = self.next_board(chessboard, ite, turn)
            chessboard[ite[0]][ite[1]] = turn
            res = self.extend(chessboard, -turn, True)
            match[idx] = [1, res]
            sb = Node()
            sub_nodes.append(sb)
            sb.n = 1
            sb.v = res
            chessboard[ite[0]][ite[1]] = 0
            for ite1 in rechange:
                chessboard[ite1[0]][ite1[1]] = -turn
            nHere += 1
        t1 = time.perf_counter()
        uct1 = [0 for i in range(len(arrivable))]
        for total in range(self.t):
            # if total%100==0:
            #     print(time.perf_counter())
            #     print(total)
            mv = -10000000
            midx = 0
            for idx, ite in enumerate(arrivable):
                rechange = self.next_board(chessboard, ite, turn)
                chessboard[ite[0]][ite[1]] = turn
                node = match[idx]
                ucts[idx] = node[1] / node[0] + self.c * ((math.log(nHere) / node[0]) ** 0.5)
                uct1[idx] = node[1] / node[0]
                if mv < ucts[idx]:
                    mv = ucts[idx]
                    midx = idx
                chessboard[ite[0]][ite[1]] = 0
                for ite1 in rechange:
                    chessboard[ite1[0]][ite1[1]] = -turn
            ite = arrivable[midx]
            rechange = self.next_board(chessboard, ite, turn)
            chessboard[ite[0]][ite[1]] = turn
            res = self.sub_mct(chessboard, -turn, True, sub_nodes[midx])
            match[midx][0] += 1
            match[midx][1] += res
            chessboard[ite[0]][ite[1]] = 0
            for ite1 in rechange:
                chessboard[ite1[0]][ite1[1]] = -turn
            nHere += 1
            if time.perf_counter() - t1 > 3.5:
                break
        midx = 0
        mv = -10000000
        for idx, ite in enumerate(arrivable):
            v = match[idx][0]
            if mv < v:
                mv = v
                midx = idx
        return arrivable[midx]

    def sub_mct(self, chessboard, turn, lastCan: bool, node: Node):
        if len(node.arrivable) == 0:
            node.arrivable = self.get_arrivable(chessboard, turn)
            random.shuffle(node.arrivable)
            arrivable = node.arrivable
        else:
            arrivable = node.arrivable
        ucts = [0 for i in range(len(arrivable))]
        s = 0
        if len(arrivable) == 0:
            my = 0
            s = 0
            for i in range(8):
                for j in range(8):
                    if chessboard[i][j] != 0:
                        s += 1
                        if chessboard[i][j] == self.color:
                            my += 1
            if s == 64:
                if my < 32:
                    return 1
                elif my == 32:
                    return 0
                else:
                    return -1
            if lastCan:
                if len(node.sub_nodes)==0:
                    sb = Node()
                    node.sub_nodes.append(sb)
                    res=self.extend(chessboard, -turn, False)
                    sb.n = 1
                    sb.v = res
                    return res
                else:
                    res=self.sub_mct(chessboard,-turn,False,node.sub_nodes[0])
                    node.n+=1
                    node.v+=res
                    return res
            else:
                if my < s / 2:
                    return 1
                elif my == s / 2:
                    return 0
                else:
                    return -1
        s = 0
        for i in range(8):
            for j in range(8):
                if chessboard[i][j] != 0:
                    s += 1
        nxt = -turn
        if nxt == -1:
            nxt = 0
        s += 1
        now = 1 if turn == 1 else 0
        # print(s,flush=True)

        mv = -10000000
        midx = 0
        for idx, ite in enumerate(arrivable):
            if len(node.sub_nodes) < idx + 1:
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
                for ite1 in rechange:
                    chessboard[ite1[0]][ite1[1]] = -turn
                return res
            else:
                sub = node.sub_nodes[idx]
                if turn != self.color:
                    ucts[idx] = self.c * ((math.log(node.n) / sub.n) ** 0.5) - sub.v / sub.n
                else:
                    ucts[idx] = self.c* ( (math.log(node.n) / sub.n) ** 0.5) + sub.v / sub.n
                if mv < ucts[idx]:
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
        for ite1 in rechange:
            chessboard[ite1[0]][ite1[1]] = -turn
        return res

    def get_mark(self, chessboard: list, nowTurn):
        ans = 0
        initial = 0
        arb = len(self.get_arrivable(chessboard, nowTurn))
        if nowTurn!=self.color:
            arb=-arb
        stable = 0
        is_stable = [[0 for i in range(8)] for j in range(8)]
        # for i in range(8):
        #     if chessboard[i][0] != 0:
        #         print("yes")
        for i in range(8):
            j = 0
            while j < 8:
                if chessboard[i][j] != 0:
                    is_stable[i][j] += 1
                else:
                    break
                j += 1
            if j < 7:
                j = 7
                while j >= 0:
                    if chessboard[i][j] != 0:
                        is_stable[i][j] += 1
                    else:
                        break
                    j -= 1
        for j in range(8):
            i = 0
            while i < 8:
                if chessboard[i][j] != 0:
                    is_stable[i][j] += 1
                else:
                    break
                i += 1

            if i < 7:
                i = 7
                while i > 0:
                    if chessboard[i][j] != 0:
                        is_stable[i][j] += 1
                    else:
                        break
                    i -= 1
        direction = (-1, 1)

        for i in range(15):
            loc = [order4[i][0], order4[i][1]]
            while self.legal(loc):
                if chessboard[loc[0]][loc[1]] != 0:
                    is_stable[loc[0]][loc[1]] += 1
                else:
                    break
                loc[0] += direction[0]
                loc[1] += direction[1]

            if self.legal(loc):
                while self.legal((loc[0] + direction[0], loc[1] + direction[1])):
                    loc[0] += direction[0]
                    loc[1] += direction[1]
                while self.legal(loc) and chessboard[loc[0]][loc[1]] != 0:
                    is_stable[loc[0]][loc[1]] += 1
                    loc[0] -= direction[0]
                    loc[1] -= direction[1]

        direction = (1, 1)
        for i in range(15):
            loc = [order5[i][0], order5[i][1]]
            while self.legal(loc):
                if chessboard[loc[0]][loc[1]] != 0:
                    is_stable[loc[0]][loc[1]] += 1
                else:
                    break
                loc[0] += direction[0]
                loc[1] += direction[1]

            if self.legal(loc):
                while self.legal((loc[0] + direction[0], loc[1] + direction[1])):
                    loc[0] += direction[0]
                    loc[1] += direction[1]
                while self.legal(loc) and chessboard[loc[0]][loc[1]] != 0:
                    is_stable[loc[0]][loc[1]] += 1
                    loc[0] -= direction[0]
                    loc[1] -= direction[1]

        for i in range(self.chessboard_size):
            for j in range(self.chessboard_size):
                if chessboard[i][j] == self.color:
                    if is_stable[i][j] >= 4:
                        stable -= 1
                    initial += self.score_matrix[i][j]
                elif (chessboard[i][j] == -self.color):
                    if is_stable[i][j] >= 4:
                        stable += 1
                    initial -= self.score_matrix[i][j]
        ans = self.c1 * initial + self.c2 * stable + self.c3 * arb
        return ans

    def extend(self, chessboard: list, turn, lastCan: bool):
        arrivable = self.get_arrivable(chessboard, turn)
        if len(arrivable) == 0:
            s = 0
            my = 0
            for i in range(8):
                for j in range(8):
                    if chessboard[i][j] != 0:
                        s += 1
                        if chessboard[i][j] == self.color:
                            my += 1
            if s == 64:
                if my < 32:
                    return 1
                elif my == 32:
                    return 0
                else:
                    return -1
            if lastCan:
                return self.extend(chessboard, -turn, False)
            else:
                if my < s / 2:
                    return 1
                elif my == s / 2:
                    return 0
                else:
                    return -1
        selection = random.randint(0, len(arrivable) - 1)
        nxt = arrivable[selection]
        rechange = self.next_board(chessboard, nxt, turn)
        chessboard[nxt[0]][nxt[1]] = turn
        out = self.extend(chessboard, -turn, True)
        chessboard[nxt[0]][nxt[1]] = 0
        for ite in rechange:
            chessboard[ite[0]][ite[1]] = -turn
        return out

    def winner_search(self, board, turnHere, deep, lastCan):
        maxDepth = 28
        sz = 0
        if ((maxDepth - deep) % 2 == 1):
            out = bigInf
        else:
            out = -bigInf
        bestLocation = -1
        res = 0
        for idx, ite in enumerate(order):
            if self.judge_move(board, turnHere, ite):
                sz = 1
                rechange = self.next_board(board, ite, turnHere)
                board[ite[0]][ite[1]] = turnHere
                nxt = self.winner_search(board, -turnHere, deep - 1, True)
                board[ite[0]][ite[1]] = 0
                for ite1 in rechange:
                    board[ite1[0]][ite1[1]] = -turnHere
                if (maxDepth - deep) % 2 == 0:
                    if nxt == bigInf:
                        if deep == maxDepth:
                            out = bigInf
                            bestLocation = idx
                            break
                        else:
                            return bigInf
                    elif nxt == 0:
                        out = 0
                        bestLocation = idx
                else:
                    if nxt == -bigInf:
                        return -bigInf
                    elif nxt == 0:
                        out = 0
        if deep == maxDepth:
            print(out)
            if bestLocation >= 0:
                out = order[bestLocation]
            else:
                return -1

        if (sz == 0):
            if deep == maxDepth:
                out = []
                return out
            sc = 0
            my = 0
            for i in range(self.chessboard_size):
                for j in range(self.chessboard_size):
                    sc += abs(board[i][j])
                    if board[i][j] == self.color:
                        my += 1
            if sc == 64:
                if my < sc / 2:
                    return bigInf
                elif my == sc / 2:
                    return 0
                else:
                    return -bigInf
            else:
                if lastCan:
                    return self.winner_search(board, -turnHere, deep - 1, False)
                else:
                    if my < sc / 2:
                        return bigInf
                    elif my == sc / 2:
                        return 0
                    else:
                        return -bigInf

        if deep == 0:
            out = self.get_mark(board,turnHere)
            return out
        return out

    def ab_search(self, board, turnHere, deep, alpha, beta, lastCan):
        if deep == 0:
            out = self.get_mark(board,turnHere)
            return out
        maxDepth = self.maxD
        sz = 0
        bestLocation = -1
        res = 0
        for idx, ite in enumerate(order2):
            if self.judge_move(board, turnHere, ite):
                sz = 1
                rechange = self.next_board(board, ite, turnHere)
                board[ite[0]][ite[1]] = turnHere
                nxt = self.ab_search(board, -turnHere, deep - 1, alpha, beta, True)
                board[ite[0]][ite[1]] = 0
                for ite1 in rechange:
                    board[ite1[0]][ite1[1]] = -turnHere
                if (maxDepth - deep) % 2 == 0:
                    if alpha < nxt:
                        alpha = nxt
                        bestLocation = idx
                    if alpha >= beta:
                        if maxDepth==deep:
                            break
                        return alpha
                else:
                    if beta > nxt:
                        beta = nxt
                    if alpha >= beta:
                        return beta
        if deep == maxDepth:
            if bestLocation >= 0:
                out = order2[bestLocation]
                return out
        if (sz == 0):
            if deep == maxDepth:
                out = []
                return out
            sc = 0
            my = 0
            for i in range(self.chessboard_size):
                for j in range(self.chessboard_size):
                    sc += abs(board[i][j])
                    if board[i][j] == self.color:
                        my += 1
            if sc == 64:
                return self.get_mark(board,turnHere)
            else:
                if lastCan:
                    return self.ab_search(board, -turnHere, deep - 1, alpha,beta,False)
                else:
                    return self.get_mark(board,turnHere)
        return alpha if (maxDepth - deep) % 2 == 0 else beta

    def go(self, chessboard):
        self.candidate_list.clear()
        self.candidate_list = self.get_arrivable(chessboard, self.color)
        s = 0
        # for i in range(8):
        #     for j in range(8):
        #         if chessboard[i][j] != 0:
        #             s += 1
        if (len(self.candidate_list) > 0):
                self.maxD = 1
                self.candidate_list.append(self.ab_search(chessboard, self.color, 1, -smallInf, smallInf, True))


def playto(black:AI,white:AI)->int:
    bd = [[0 for i in range(8)] for j in range(8)]
    bd[3][3] = COLOR_WHITE
    bd[3][4] = COLOR_BLACK
    bd[4][3] = COLOR_BLACK
    bd[4][4] = COLOR_WHITE
    for t in range(61):
        if t % 2 == 0:
            black.go(bd)
            c=black.candidate_list
            if len(c)>0:
                p=c[len(c)-1]
                black.next_board(bd,p,COLOR_BLACK)
                bd[p[0]][p[1]]=COLOR_BLACK
        else:
            white.go(bd)
            c = white.candidate_list
            if len(c) > 0:
                p = c[len(c) - 1]
                white.next_board(bd, c[len(c) - 1], COLOR_WHITE)
                bd[p[0]][p[1]] = COLOR_WHITE
    total = 0
    black_num = 0
    for i in range(8):
        for j in range(8):
            total += abs(bd[i][j])
            if bd[i][j] == COLOR_BLACK:
                black_num += 1
    if black_num < total/2:
        return 1
    elif black_num == total/2:
        return 0
    else:
        return -1

def translate(chessboard,loc):
    x=loc[0]
    y=loc[1]
    chessboard[x][7-y]=chessboard[7-x][y]=chessboard[7-x][7-y]=chessboard[x][y]

def product(waiters:list):
    l = len(waiters)
    for i in range(l):
        waiter=waiters[i]
        waiter:AI
        mate:AI=waiters[(i+random.randint(0,l-1))%l]
        son=AI(8,0,100)
        son.c1=waiter.c1 if random.randint(0,100)%2==0 else mate.c1
        if random.randint(0,100000) % 100 ==0:
            son.c1 += random.randint(-5,5)
        son.c2=waiter.c2 if random.randint(0,100)%2==0 else mate.c2
        if random.randint(0,100000) % 100 ==0:
            son.c2 += random.randint(-5,5)
        son.c3=waiter.c3 if random.randint(0,100)%2==0 else mate.c3
        if random.randint(0,100000) % 100 ==0:
            son.c3 += random.randint(-5,5)
        for row in range(4):
            for column in range(row+1):
                son.score_matrix[row][column]=waiter.score_matrix[row][column] if random.randint(0,100)%2==0 else mate.score_matrix[row][column]
                if random.randint(0, 100000) % 100 == 0:
                    son.score_matrix[row][column] += random.randint(-5, 5)
                son.score_matrix[column][row]=son.score_matrix[row][column]
                translate(son.score_matrix,[row,column])
                translate(son.score_matrix,[column,row])
        waiters.append(son)






def inheritance(waiters:list):
    random.seed()
    random.shuffle(waiters)
    for player in waiters:
        player:AI
        player.win_num = 0
        player.tie_num=0
    for idx,black_player in enumerate(waiters):
        # t=time.perf_counter()
        for j in range(1,playNum+1):
            white_player=waiters[(idx+j) % waiter_num]
            black_player.color=COLOR_BLACK
            white_player.color=COLOR_WHITE
            res = playto(black_player,white_player)
            if res == 1:
                black_player:AI
                black_player.win_num += 1
            elif res == -1:
                white_player:AI
                white_player.win_num += 1
            else:
                black_player.tie_num+=1
                white_player.tie_num+=1
        # print(time.perf_counter()-t)
    list.sort(waiters,key=lambda ai:(ai.win_num,ai.tie_num),reverse=True)
    for t in range(int(waiter_num/2)):
        waiters.pop()
    winner:AI=waiters[0]
    print(winner.score_matrix)
    print((winner.c1,winner.c2,winner.c3))
    product(waiters)
    # for i in range(int(waiter_num/2)):


if __name__ == "__main__":
    file1 = open("cores_control.txt", mode="r")
    s1 = file1.readline()
    cores = int(s1)
    print(cores)
    # random.seed()
    # playNum=5
    # waiter_num=200
    # total = 0
    # waiters=[]
    # for i in range(waiter_num):
    #     here=AI(8,0,100)
    #     waiters.append(here)
    #     for row in range(4):
    #         for column in range(row+1):
    #             here.score_matrix[row][column]=random.randint(-300,300)
    #             here.score_matrix[column][row] = here.score_matrix[row][column]
    #             translate(here.score_matrix, [row, column])
    #             translate(here.score_matrix, [column, row])
    #     here.c1=random.randint(-10,10)
    #     here.c2=random.randint(-1000,1000)
    #     here.c3=random.randint(-1000,1000)
    # while True:
    #     inheritance(waiters)
    #     total+=1
    #     print(f"total:{total}")







