from Programma.UDPP.Local import udppLocal
from Programma.UDPP.Local.udppLocal import udpp_local
from Programma.UDPP.LocalOptimised.udppLocalOpt import UDPPlocalOpt
from data import dfMaker
from Programma.MaxBenefit import maxBenefit

from Programma.Istop import istop

from Programma.ModelStructure.Costs.costFunctionDict import CostFuns
from Programma.UDPP import udppModel
import random
import pandas as pd

# df = pd.read_csv("../data/data_ruiz.csv")
scheduleType = dfMaker.schedule_types(show=True)
df = pd.read_csv("dfcrash")
# df = dfMaker.df_maker(40, 5, distribution=scheduleType[0])
# df["margins"] = [random.choice(range(10, 50)) for i in range(df.shape[0])]
# df.to_csv("dfcrash")
df_max = df.copy(deep=True)
df_UDPP = df_max.copy(deep=True)

costFun = CostFuns().costFun["step"]


udMod = udppModel.UDPPmodel(df_UDPP, costFun)
air = udMod.airlines[0]



# for f in air.flights:
#     print(f, f.slot, f.newSlot, f.priorityValue, f.priorityNumber)
# print(udMod.compute_costs(air.flights, "initial"))
# UDPPlocalOpt(air, udMod.slots)
udMod.run(optimised=True)
udMod.print_performance()
#print(udMod.compute_costs(air.flights, "final"))


# for f in air.flights:
#     print(f, f.slot, f.newSlot.time, f.priorityValue, f.cost, f.margin)

print(udMod.compute_costs(air.flights,"initial"))
print(udMod.compute_costs(air.flights,"final"))

# udpp_local(air, udMod.slots)
udMod.run()
udMod.print_performance()

print("\n")




# for f in air.flights:
#     print(f, f.slot, f.newSlot.time, f.priorityValue, f.cost, f.margin, f.priorityNumber)
print(udMod.compute_costs(air.flights,"initial"))
print(udMod.compute_costs(air.flights,"final"))






