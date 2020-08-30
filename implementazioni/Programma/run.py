import time
from data import dfMaker
import pandas as pd
from Programma.Mip import mipModel
from Programma.Amal import amal
from Programma.UDPP import udppModel
from Programma.Max_benefit import max_benefit
import numpy as np
from mip import *

# df = pd.read_csv("../data/data_ruiz.csv")


total_initial = []
total_max_ben = []
total_udpp = []
total_model = []

infeasible = 0
distribution = "increasing"
num_airlines = 20
num_fligths = 70
for alpha in [0.5]:  # 0.25, 0.5, 0.75,
    print("alpha ", alpha)
    for i in range(63, 70):
        try:
            simulations = pd.DataFrame(
                columns=["run", "airline", "num_flights", "initial", "max_reduction", "udpp", "model", "offers"])
            t = time.time()
            print("iterazione ******** ", i)
            df = dfMaker.df_maker(num_fligths, num_airlines, distribution=distribution)
            df_max = df.copy(deep=True)
            df_amal = df.copy(deep=True)
            df_UDPP = df_amal.copy(deep=True)
            # print(df)

            max_model = max_benefit.MaxBenefitModel(df_max)
            max_model.run()
            mmr = max_model.report.copy(deep=True)
            print("max benefit")

            udpp_model = udppModel.UDPPModel(df_UDPP)
            udppr = udpp_model.report.copy(deep=True)
            print("udpp")

            model = mipModel.MipModel(udpp_model.get_new_df(), 1)
            model.run()

            print("model")
            # print(model.offers)
            # model1 = mipModel.MipModel(df, 0)
            # model1.run()
            # print("con base")
            # print(model1.offers)
            # print(model1.df[["flight", "new slot", "new arrival", "eta slot", "cost", "num"]])

            total_initial.append(max_model.report["initial costs"][0])
            total_max_ben.append(max_model.report["final costs"][0])
            total_udpp.append(udpp_model.report["final costs"][0])
            total_model.append(model.report["final costs"][0])

            omr = model.report
            offer = model.offers

            simulations = simulations.append(pd.Series([i, "total", num_fligths, mmr["initial costs"][0],
                                                        mmr["final costs"][0], udppr["final costs"][0],
                                                        omr["final costs"][0], offer["offers"][0]],
                                                       index=simulations.columns),
                                             ignore_index=True)

            for airline in mmr["airline"][1:]:
                air_num_flights = df[df["airline"] == airline].shape[0]
                simulations = simulations.append(pd.Series([i, airline, air_num_flights,
                                                            mmr[mmr["airline"] == airline]["initial costs"].values[0],
                                                            mmr[mmr["airline"] == airline]["final costs"].values[0],
                                                            udppr[udppr["airline"] == airline]["final costs"].values[0],
                                                            omr[omr["airline"] == airline]["final costs"].values[0],
                                                            offer[offer["airline"] == airline]["offers"].values[0]],
                                                           index=simulations.columns),
                                                 ignore_index=True)
            print(model.offers.iloc[0])
            print(time.time() - t)
            if model.m.status == OptimizationStatus.OPTIMAL or model.m.status == OptimizationStatus.FEASIBLE:
                if i == 0:
                    # print(simulations[["num flights", "initial", "max_reduction", "udpp", "model", "offers"]])
                    simulations.to_csv("../results/" + str(num_fligths) + "_" + str(alpha) + ".csv", index=False)

                else:
                    simulations.to_csv("../results/" + str(num_fligths) + "_" + str(alpha) + ".csv",
                                           mode='a', header=False, index=False)
            else:
                infeasible += 1
                print("infeasible   :", infeasible)

        except:
            print("************************************************************************************")

