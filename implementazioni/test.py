from airline import *
from model_1 import *
from model_2 import *

import numpy as np



# BA=airline("BA",[1,4,5],[4,9,12])
# YA=airline("YA",[0,2,3,6],[1,14,1,15])
# ETA=np.array(range(7))
# FPFS=ETA*2

# BA = airline("BA", [1, 4, 5], [1, 20, 1])
# YA = airline("YA", [0, 2, 3, 6], [1, 14, 1, 1])
# ETA = np.array(range(7))
# FPFS = ETA * 8
#
# problem = model_2([BA, YA], ETA, FPFS)
# problem.run()
#
# problem.print_schedule()
# problem.print_solution()
#
# for l in problem.solutionC:
#     row = []
#     for c in l:
#         row.append(c.x)
#     print(row)
#
# for i in problem.slots:
#     row = []
#     for j in problem.slots:
#         row.append(problem.solutionX[i, j].x)
#     print(row)


BA = airline("BA", [1, 4, 5], [4, 9, 12])
YA = airline("YA", [0, 2, 3, 6], [1, 14, 1, 15])
ETA = np.array(range(7))
FPFS = ETA * 2

problem = model_2([BA, YA], ETA, FPFS)
problem.run()



problem.print_offers()
