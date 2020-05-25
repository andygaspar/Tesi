from data import dfMaker
import pandas as pd
from Programma.Mip import mipModel
from Programma.Amal import amal
from Programma.UDPP import udppModel
from Programma.Max_benefit import max_benefit
import numpy as np

# df = pd.read_csv("../data/data_ruiz.csv")



df_max = dfMaker.df_maker(70, 10, distribution="uniform")
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





# slot = np.array(range(15))
# eta = slot
# airline = ["A","C","B","A","B","A","B","C","B","C","A","A","B","C","A"]
# cost =    [8 , 1 , 6  , 5 ,10 , 7 , 4 , 2 ,10 , 3 ,21 , 9 , 11 , 2 , 15]
# flights = [airline[i]+str(i) for i in range(len(airline))]
# gdp = eta * 2
#
# priority = cost
#
#
# df = pd.DataFrame({"slot": slot, "flight": flights, "eta": eta, "gdp schedule": gdp, "priority": priority, "airline": airline,
#          "cost": cost})