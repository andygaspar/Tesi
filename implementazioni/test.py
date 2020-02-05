import airline as air
import model_1 as mod_1
import model_2 as mod_2

import numpy as np


BA=air.airline("BA",[1,4,5],[4,9,12])
YA=air.airline("YA",[0,2,3,6],[1,14,1,15])

ETA=np.array(range(7))
FPFS=ETA*2


problem_1=mod_1.model_1([BA,YA],ETA,FPFS)
problem_1.run()


problem=mod_2.model_2([BA,YA],ETA,FPFS)
problem.run()

problem.print_schedule()
problem_1.print_solution()
problem.print_solution()
problem_1.print_offers()
problem.print_offers()
