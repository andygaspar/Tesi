from data import dfMaker
import pandas as pd
from Programma.Mip import mipModel
from Programma.Amal import amal
from Programma.UDPP import udppModel
from Programma.Max_benefit import max_benefit

# df = pd.read_csv("../data/data_ruiz.csv")



df_max = dfMaker.df_maker(35, 5, distribution="uniform")
df_amal = df_max.copy(deep=True)
df_UDPP = df_amal.copy(deep=True)
print(df_max)

max_model = max_benefit.MaxBenefitModel(df_max)
max_model.run()

amal_model = amal.Amal(df_amal, offerMakerFunType="1")
amal_model.run()

udpp_model = udppModel.UDPPModel(df_UDPP)

model = mipModel.MipModel(udpp_model.get_new_df())
model.run()


