from data import dfMaker
import pandas as pd
from Programma.Mip import mipModel
from Programma.Amal import amal



# df = pd.read_csv("data/sample.csv")
# df["priority"] = df["cost"]
df = pd.read_csv("../data/data_ruiz.csv")

df_init = df.iloc[0:30]

print(df.airline.unique())

df = dfMaker.df_maker(20, 3)
print(df)

model = mipModel.MipModel(df)

model.run()
#
#
#print(model.solution)
print("*****+ AMAL *****************++")
amal_model = amal.Amal(df, offerMakerFunType="1")
amal_model.run()
# print(model.solution.airline_balance)
# print(model.initial_objective_value)
# print(model.m.objective_value)
# print(model.solution.offers)




# int_df = pd.read_csv("data/sample.csv")
#
# model = MipModel(int_df)
#
# model.run()

# print(model.solution_df)
# print(model.print_offers())

#************************************************************************************
#8,HUB 5701,756,757,25,HUB     sarebbe  8,HUB 5701,756,756,25,HUB
#************************************************************************************


