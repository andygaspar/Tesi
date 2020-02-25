import numpy as np
import pandas as pd
from Mip import mipModel


df = pd.read_csv("ruiz.csv")
df["cost"] = np.random.uniform(1, 15, df.shape[0])

df_init = df.iloc[0:44]

model = mipModel.MipModel(df_init)

model.run()

# int_df = pd.read_csv("data/sample.csv")
#
# model = MipModel(int_df)
#
# model.run()

# print(model.solution_df)
# print(model.print_offers())

#8,HUB 5701,756,757,25,HUB     sarebbe  8,HUB 5701,756,756,25,HUB