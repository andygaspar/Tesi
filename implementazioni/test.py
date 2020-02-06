from airline import *
from model_1 import *
from model2 import *

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


BA = Airline("BA", [1, 4, 5], [4, 9, 12], costs=[4, 9, 12])
YA = Airline("YA", [0, 2, 3, 6], [1, 14, 1, 15], costs=[1, 14, 1, 15])


ETA = np.array(range(100,107))
FPFS = ETA + range(0,7)

problem = Model2([BA, YA], ETA, FPFS)

problem.run()

problem.print_schedule()
problem.print_solution()

problem.print_offers()


ETA = np.array(range(7))
FPFS = ETA*2

problem = Model2([BA, YA], ETA, FPFS)
problem.run()

problem.print_schedule()
problem.print_solution()

problem.print_offers()
