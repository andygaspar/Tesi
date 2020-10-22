from data import dfMaker
import pandas as pd
from Programma.Max_benefit import max_benefit
from Programma.Istop import istop
from Programma.Istop import istopXpress

from Programma.ModelStructure.Costs.costFunctionDict import CostFuns
from Programma.UDPP import udppModel

# df = pd.read_csv("../data/data_ruiz.csv")
df = dfMaker.df_maker(15, 2, distribution="uniform")

df_max = df.copy(deep=True)
df_UDPP = df_max.copy(deep=True)

costFun = CostFuns().costFun["quadratic"]
# max_model = max_benefit.MaxBenefitModel(df_max, costFun)
# max_model.run()
# max_model.print_performance()


# udpp_model = udppModel.UDPPModel(df_UDPP, costFun)
# udpp_model.print_performance()

# model = istop.Istop(udpp_model.get_new_df(), costFun)
model = istop.Istop(df_max, costFun)
model.run()
model.print_performance()


# xpModel = istopXpress.IstopXpress(udpp_model.get_new_df(), costFun)
xpModel = istopXpress.IstopXpress(df_max, costFun)
xpModel.run()
xpModel.print_performance()

