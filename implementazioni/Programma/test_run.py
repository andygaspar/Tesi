from data import dfMaker
import pandas as pd
from Programma.Mip import mipModel
from Programma.Amal import amal
from Programma.UDPP import udppModel

# df = pd.read_csv("../data/data_ruiz.csv")

df_UDPP = dfMaker.df_maker(30, 5, distribution="uniform")

udpp_model = udppModel.UDPPModel(df_UDPP)

print(udpp_model.get_new_df()[["flight", "new slot", "new arrival", "eta slot", "cost"]])

# model = mipModel.MipModel(udpp_model.get_new_df())
# model.run()
