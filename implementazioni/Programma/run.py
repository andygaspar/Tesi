from data import dfMaker
import pandas as pd
from Programma.Mip import mipModel
from Programma.Amal import amal
from Programma.UDPP import udppModel

# df = pd.read_csv("../data/data_ruiz.csv")

df_amal = dfMaker.df_maker(30, 5, distribution="few_high")
df_UDPP = df_amal.copy(deep=True)
print(df_amal)

amal_model = amal.Amal(df_amal, offerMakerFunType="1")
amal_model.run()
#
# udpp_model = udppModel.UDPPModel(df_UDPP)
#
# model = mipModel.MipModel(udpp_model.get_new_df())
# model.run()


