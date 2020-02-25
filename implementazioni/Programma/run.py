import numpy as np
import pandas as pd
from Programma.Mip import mipModel
import os


df = pd.read_csv("Programma/ruiz.csv")
df["cost"] = np.random.uniform(1, 15, df.shape[0])

df_init = df.iloc[0:20]

model = mipModel.MipModel(df_init)

model.run()


# print(model.solution)
# print(model.solution.airline_balance)
# print(model.initial_objective_value)
# print(model.m.objective_value)
print(model.solution.offers)
#
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