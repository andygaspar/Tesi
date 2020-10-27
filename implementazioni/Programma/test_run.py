from data import dfMaker
from Programma.MaxBenefit import maxBenefit

from Programma.Istop import istop

from Programma.ModelStructure.Costs.costFunctionDict import CostFuns
from Programma.UDPP import udppModelOpt
import random
import pandas as pd

# df = pd.read_csv("../data/data_ruiz.csv")
scheduleType = dfMaker.schedule_types(show=True)
df = pd.read_csv("dfcrash")
print(df)
# df = dfMaker.df_maker(40, 5, distribution=scheduleType[0])
# df["margins"] = [random.choice(range(10, 50)) for i in range(df.shape[0])]
# df.to_csv("dfcrash")
df_max = df.copy(deep=True)
df_UDPP = df_max.copy(deep=True)

costFun = CostFuns().costFun["step"]
# max_model = max_benefit.MaxBenefitModel(df_max, costFun)
# max_model.run()
# max_model.print_performance()


max_model = maxBenefit.MaxBenefitModel(df_max, costFun)
max_model.run()
max_model.print_performance()

# udpp_model = udppModel.UDPPModel(df_UDPP, costFun)
# udpp_model.print_performance()

udpp_model_xp = udppModelOpt.UDPPModelOpt(df_UDPP, costFun)
udpp_model_xp.print_performance()


# model = istop.Istop(udpp_model_xp.get_new_df(), costFun)
# # model = istop.Istop(df_max, costFun)
# model.run(True)
# model.print_performance()

xpModel = istop.Istop(udpp_model_xp.get_new_df(), costFun)
# xpModel = istopXpress.IstopXpress(df_max, costFun)
xpModel.run(True)
xpModel.print_performance()



