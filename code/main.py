import numpy as np
import random
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)


score_matrix=[[-35, 2.1999999999999993, -2.869999999999994, -0.16249999999999995, -0.16249999999999995, -2.869999999999994, 2.1999999999999993, -35],
[2.1999999999999993, -2.869999999999994, -0.16249999999999995, -1.1, -1.1, -0.16249999999999995, -2.869999999999994, 2.1999999999999993],
[-2.869999999999994, -0.16249999999999995, -1.1, -0.988, -0.988, -1.1, -0.16249999999999995, -2.869999999999994],
[-0.16249999999999995, -1.1, -0.988, -1.00144, -1.00144, -0.988, -1.1, -0.16249999999999995],
[-0.16249999999999995, -1.1, -0.988, -1.00144, -1.00144, -0.988, -1.1, -0.16249999999999995],
[-2.869999999999994, -0.16249999999999995, -1.1, -0.988, -0.988, -1.1, -0.16249999999999995, -2.869999999999994],
[2.1999999999999993, -2.869999999999994, -0.16249999999999995, -1.1, -1.1, -0.16249999999999995, -2.869999999999994, 2.1999999999999993],
[-35, 2.1999999999999993, -2.869999999999994, -0.16249999999999995, -0.16249999999999995, -2.869999999999994, 2.1999999999999993, -35],
]
score_matrix_white= [[-105, 16.999999999999996, -7.060000000000012, 0.9829999999999994, 0.9829999999999994, -7.060000000000012, 16.999999999999996, -105],
[16.999999999999996, -7.060000000000012, 0.9829999999999994, -1, -1, 0.9829999999999994, -7.060000000000012, 16.999999999999996],
[-7.060000000000012, 0.9829999999999994, -1, -1, -1, -1, 0.9829999999999994, -7.060000000000012],
[0.9829999999999994, -1, -1, -1, -1, -1, -1, 0.9829999999999994],
[0.9829999999999994, -1, -1, -1, -1, -1, -1, 0.9829999999999994],
[-7.060000000000012, 0.9829999999999994, -1, -1, -1, -1, 0.9829999999999994, -7.060000000000012],
[16.999999999999996, -7.060000000000012, 0.9829999999999994, -1, -1, 0.9829999999999994, -7.060000000000012, 16.999999999999996],
[-105, 16.999999999999996, -7.060000000000012, 0.9829999999999994, 0.9829999999999994, -7.060000000000012, 16.999999999999996, -105]]
# score_matrix =[[-67, 31.599999999999998, -8.460000000000003, 1.6260000000000006, 1.6260000000000006, -8.460000000000003, 31.599999999999998, -67],
# [31.599999999999998, -8.460000000000003, 1.6260000000000006, -1, -1, 1.6260000000000006, -8.460000000000003, 31.599999999999998],
# [-8.460000000000003, 1.6260000000000006, -1, -1, -1, -1, 1.6260000000000006, -8.460000000000003],
# [1.6260000000000006, -1, -1, -1, -1, -1, -1, 1.6260000000000006],
# [1.6260000000000006, -1, -1, -1, -1, -1, -1, 1.6260000000000006],
# [-8.460000000000003, 1.6260000000000006, -1, -1, -1, -1, 1.6260000000000006, -8.460000000000003],
# [31.599999999999998, -8.460000000000003, 1.6260000000000006, -1, -1, 1.6260000000000006, -8.460000000000003, 31.599999999999998],
# [-67, 31.599999999999998, -8.460000000000003, 1.6260000000000006, 1.6260000000000006, -8.460000000000003, 31.599999999999998, -67]]


# global score_matrix


# don't change the class name
class AI(object):
    # chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
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


    def legal(self,p):
        if ((p[0] >= 0 and p[0] <self.chessboard_size) and (p[1] >= 0 and p[1] < self.chessboard_size)):
            return True
        return False


    def get_arrivable(self,chessboard: list, turn)->list:
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

    def get_mark(self, chessboard: list):
        ans = 0
        for i in range(self.chessboard_size):
            for j in range(self.chessboard_size):
                if chessboard[i][j] == self.color:
                    if(self.color==COLOR_BLACK):
                        ans += score_matrix[i][j]
                    else:
                        ans += score_matrix_white[i][j]
                elif (chessboard[i][j] == -self.color):
                    if(self.color==COLOR_BLACK):
                        ans -= score_matrix[i][j]
                    else:
                        ans-=score_matrix_white[i][j]
        return ans

    def next_board(self, board: list, point: list, turnHere: int):
        dir = [[1, 0],
               [-1, 0],
               [0, 1],
               [0, -1],
               [1, 1],
               [-1, - 1],
               [1, -1],
               [-1, 1]]
        nextBoard = board
        loc = [0,0]
        for iHere in range(8):
            loc[0] = point[0]
            loc[1] = point[1]
            while loc[0] < self.chessboard_size and loc[0] >= 0 and loc[1] < self.chessboard_size and loc[1] > 0:
                if (board[loc[0]][loc[1]] == turnHere):
                    while (not (loc[0] == point[0] and loc[1] == point[1])):
                        nextBoard[loc[0]][loc[1]] = turnHere
                        loc[0] = loc[0] - dir[iHere][0]
                        loc[1] = loc[1] - dir[iHere][1]
                    break
                else:
                    if board[loc[0]][loc[1]] == 0 and (not (loc[0] == point[0] and loc[1] == point[1])):
                        break
                loc[0] = loc[0] + dir[iHere][0]
                loc[1] = loc[1] + dir[iHere][1]


    def ab_search(self,board,turnHere,deep,alpha,beta):
        maxDepth = 3
        arrivable = self.get_arrivable(board, turnHere)

        sz = len(arrivable)
        if (sz == 0):
            if deep==maxDepth:
                out=[]
                return out
            if (maxDepth-deep)%2==0:
                sc=0
                my=0
                for i in range(self.chessboard_size):
                    for j in range(self.chessboard_size):
                        sc+=abs(board[i][j])
                        if board[i][j]==self.color:
                            my+=1
                if sc==self.chessboard_size*self.chessboard_size:
                    if my<self.chessboard_size*self.chessboard_size/2:
                        return 100000
                    else:
                        return -100000
                return 100000
            else:
                sc = 0
                my = 0
                for i in range(self.chessboard_size):
                    for j in range(self.chessboard_size):
                        sc += abs(board[i][j])
                        if board[i][j] == self.color:
                            my += 1
                if sc==self.chessboard_size*self.chessboard_size:
                    if my<self.chessboard_size*self.chessboard_size/2:
                        return 100000
                    else:
                        return -100000
                return -100000
        cpBoard = [[ 0 for i in range(self.chessboard_size)] for j in range(self.chessboard_size)]
        rate = 0
        next = 0
        bestLocation = 0

        if(deep==maxDepth):out=[]
        else:out=0
        if (deep == 0):
            out = self.get_mark(board)
        else:
            for i in range(sz):
                for j in range(self.chessboard_size):
                    for k in range(self.chessboard_size):
                        cpBoard[j][k] = board[j][k]
                self.next_board(cpBoard, arrivable[i], turnHere)
                cpBoard[arrivable[i][0]][arrivable[i][1]] = turnHere
                if (turnHere == -1):
                    next = self.ab_search(cpBoard, 1, deep - 1, alpha, beta)
                else:
                    next = self.ab_search(cpBoard, -1, deep - 1, alpha, beta)
                if ((maxDepth - deep) % 2 == 0):
                    out = alpha
                    if (alpha < next):
                        alpha = next
                        out = alpha
                        bestLocation = i
                    elif alpha==next:
                        if random.randint(0,10)%3==0:
                            bestLocation = i
                    if (alpha > beta):
                        return alpha

                else:
                    out = beta
                    if (beta > next):
                        beta = next
                        out = beta
                    if (alpha > beta):
                        return beta
        if (deep == maxDepth):
            out = arrivable[bestLocation]
        return out
    def go(self, chessboard):
        # Clear candidate_list, must do this step
        self.candidate_list.clear()
        # Write your algorithm here
        # Here is the simplest sample:Random decision
        # idx = np.where(chessboard == COLOR_NONE)
        # idx = list(zip(idx[0], idx[1]))
        self.candidate_list=self.get_arrivable(chessboard,self.color)
        if(len(self.candidate_list)>0):
            self.candidate_list.append(self.ab_search(board=chessboard,turnHere=self.color,deep=3,alpha=-1000000,beta=1000000))

#
#         # ==============Find new pos========================================
#         # Make sure that the position of your decision in chess board is empty.
#         # If not, the system will return error.
#         # Add your decision into candidate_list, Records the chess board
#         # You need add all the positions which is valid
#         # candiidate_list example: [(3,3),(4,4)]
#         # You need append your decision at the end of the candiidate_list,
#         # we will choice the last element of the candidate_list as the position you choose
#         # If there is no valid position, you must return an empty list.
#
#
# if __name__ == "__main__":
#     # global score_matrix
#     bd = [[0 for i in range(8)] for j in range(8)]
#     bd[3][3]=-1
#     bd[3][4]=1
#     bd[4][3]=1
#     bd[4][4]=-1
    # bd[3][2]=-1
    # bd[]
    # a=AI(8,1,180)
    # # a.go(bd)
    # # c=a.candidate_list[len(a.candidate_list)-1]
    # # a.next_board(bd, c, 1)
    # # bd[c[0]][c[1]]=1
    # print("en")
    # for i in range(30):
    #     print("yes")
    #     if i%2==0:
    #         a=AI(8,1,180)
    #         a.go(bd)
    #         c=a.candidate_list[len(a.candidate_list)-1]
    #         a.next_board(bd, c, 1)
    #         bd[c[0]][c[1]]=1
    #     else:
    #         a = AI(8, -1, 180)
    #         a.go(bd)
    #         c = a.candidate_list[len(a.candidate_list) - 1]
    #         a.next_board(bd,c,-1)
    #         bd[c[0]][c[1]] = -1

    # for i in range(4,8):
    #     for j in range(8):
    #         bd[i][j]=-1
    # bd[7][7]=0



#     lis = [1, 2]
#     b = lis
#     b[1] = 200
#     print(lis)
#     for i in range(8):
#         for j in range(8):
#             score_matrix[i][j]=-score_matrix[i][j]
#     print(score_matrix)
