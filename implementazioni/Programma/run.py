from data import dfMaker
import pandas as pd
from Programma.Mip import mipModel
from Programma.Amal import amal
from Programma.UDPP import udppModel
from Programma.Max_benefit import max_benefit
import numpy as np

# df = pd.read_csv("../data/data_ruiz.csv")

total_initial = []
total_max_ben = []
total_udpp = []
total_model = []


for i in range(10):
    print("iterazione ******** ",i)
    df_max = dfMaker.df_maker(50, 10, distribution="increasing")
    df_amal = df_max.copy(deep=True)
    df_UDPP = df_amal.copy(deep=True)

    #print(df_max)

    max_model = max_benefit.MaxBenefitModel(df_max)
    max_model.run()

    #amal_model = amal.Amal(df_amal, offerMakerFunType="1")
    #amal_model.run()

    udpp_model = udppModel.UDPPModel(df_UDPP)

    model = mipModel.MipModel(udpp_model.get_new_df())
    model.run()

    total_initial.append(max_model.report["initial costs"][0])
    total_max_ben.append(max_model.report["final costs"][0])
    total_udpp.append(udpp_model.report["final costs"][0])
    total_model.append(model.report["final costs"][0])

import matplotlib.pyplot as plt

plt.plot(total_initial, label="inital")
plt.plot(total_max_ben, label="max benefit")
plt.plot(total_udpp, label="udpp")
plt.plot(total_model, label="model")
plt.legend()
plt.show()



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