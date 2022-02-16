import cmath

import numpy
import numpy as np
import random
import time
import math

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)





if __name__ == "__main__" :
    # t=time.time()
    # for i in range(1000000):
    #     li=1
    # print(time.time()-t)

    # for i in range(8):
    #     for j in range(8):
    #         if (i,j) not in order2:
    #             print((i,j))
    # print(len(order2),flush=True)

    times1 = 30000
    winner = 0
    delta = 0.1
    a = 0
    heiT = 0
    baiT = 0
    last_white = -1
    last_black = -1
    black_wins = 0
    white_wins = 0
    c1 = 2
    c2 = 2
    need = False
    while a < times1 :
        need = False
        s = [[[0 for k in range(8)] for j in range(8)] for i in range(64)]
        bd = [[0 for i in range(8)] for j in range(8)]
        sc = 0
        hei = AI(8, COLOR_BLACK, 100)
        bai = AI(8, COLOR_WHITE, 100)
        bd[3][3] = COLOR_WHITE
        bd[3][4] = COLOR_BLACK
        bd[4][3] = COLOR_BLACK
        bd[4][4] = COLOR_WHITE




        for k in range(61) :
            winner = 0
            if k % 2 == 1 :
                hei.go(bd)
                lis = []
                if len(hei.candidate_list) > 0 :
                    c = hei.candidate_list[len(hei.candidate_list) - 1]
                    if c[len(c) - 1] == 100 :
                        # need=True
                        hei.next_board(bd, [c[0][0], c[0][1]], COLOR_BLACK)
                        bd[c[0][0]][c[0][1]] = COLOR_BLACK
                    else :
                        hei.next_board(bd, c, COLOR_BLACK)
                        bd[c[0]][c[1]] = COLOR_BLACK
            else :
                bai.go(bd)
                if len(bai.candidate_list) > 0 :
                    print(len(bai.candidate_list))
                    c = bai.candidate_list[len(bai.candidate_list) - 1]
                    # c = bai.candidate_list[len(bai.candidate_list) - 1]
                    bd[c[0]][c[1]] = COLOR_WHITE
            # print(bd)
            for i in range(8) :
                for j in range(8) :
                    s[k][i][j] = bd[i][j]
        # print(time.perf_counter() - t)
        for i in range(8) :
            for j in range(8) :
                if bd[i][j] == COLOR_BLACK :
                    sc += 1
        if sc < 32 :
            winner = COLOR_BLACK
            if need :
                for ite in s :
                    print(ite)
                    print()
                break
            black_wins += 1
            # c2+=delta
            last_black = c1
        elif sc > 32 :
            winner = COLOR_WHITE
            white_wins += 1
            # c1+=delta
            last_white = c2
        else :
            c2 += 0
        a += 1
        if winner == COLOR_BLACK :
            print(f"{a / times1 * 100}%,winner:black", flush=True)
        elif winner == COLOR_WHITE :
            print(f"{a / times1 * 100}%,winner:white", flush=True)
        else :
            print(f"{a / times1 * 100}%,winner:none", flush=True)
        break
    # print(heiT)
    # print(baiT)
    # print(score_matrixBai)
    print(last_white)
    print(last_black)
    print(f"black wins:{black_wins}")
    print(f"white wins:{white_wins}")

    # for i in range(8):
    # print(bd[i])

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
