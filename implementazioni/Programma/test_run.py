from data import dfMaker
import pandas as pd
from Programma.Max_benefit import max_benefit
from Programma.Istop import istop

from Programma.ModelStructure.Costs.costFunctionDict import CostFuns
from Programma.UDPP import udppModel

# df = pd.read_csv("../data/data_ruiz.csv")
df = dfMaker.df_maker(30, 5, distribution="uniform")
df_max = df.copy(deep=True)
df_UDPP = df_max.copy(deep=True)

# print(df)
costFun = CostFuns().costFun["quadratic"]
# max_model = max_benefit.MaxBenefitModel(df_max, costFun)
# max_model.run()
#
#
# udpp_model = udppModel.UDPPModel(df_UDPP, costFun)

# print(udpp_model.get_new_df()[["flight", "new slot", "new arrival", "eta slot", "cost"]])

# model = istop.Istop(udpp_model.get_new_df())
model = istop.Istop(df, costFun)
model.run()
