from data import dfMaker
from Programma.MaxBenefit import maxBenefit


from Programma.Istop import istop

from Programma.ModelStructure.Costs.costFunctionDict import CostFuns
from Programma.UDPP import udppModel
import random
import pandas as pd

# df = pd.read_csv("../data/data_ruiz.csv")
scheduleType = dfMaker.schedule_types(show=True)
# df = pd.read_csv("dfcrash")
simulations = pd.DataFrame(columns=["run", "airline", " num flights", "initial","max_reduction", "udpp", "from udpp","model", "offers"])
total_initial = []
total_max_ben = []
total_from_udpp = []
total_udpp = []
total_model = []
num_flights = 50

for i in range(40):
    try:
        df = dfMaker.df_maker(num_flights, 5, distribution=scheduleType[3])
        df["margins"] = [random.choice(range(10, 50)) for i in range(df.shape[0])]
        # df.to_csv("dfcrash")
        df_max = df.copy(deep=True)
        df_UDPP = df_max.copy(deep=True)

        costFun = CostFuns().costFun["step"]


        print("max from FPFS")
        max_model = maxBenefit.MaxBenefitModel(df_max, costFun)
        max_model.run()
        max_model.print_performance()

        print("UDPP Opt from FPFS")
        udpp_model_xp = udppModel.UDPPmodel(df_UDPP, costFun)
        udpp_model_xp.run(optimised=True)
        udpp_model_xp.print_performance()

        print("max from UDPP")
        maxFromUDPP = maxBenefit.MaxBenefitModel(udpp_model_xp.get_new_df(), costFun)
        maxFromUDPP.run()
        maxFromUDPP.print_performance()

        print("istop from UDPP")
        xpModel = istop.Istop(udpp_model_xp.get_new_df(), costFun)
        xpModel.run(True)
        xpModel.print_performance()

        total_initial.append(max_model.report["initial costs"][0])

        total_max_ben.append(max_model.report["final costs"][0])
        total_from_udpp.append(maxFromUDPP.report["final costs"][0])
        total_udpp.append(udpp_model_xp.report["final costs"][0])
        total_model.append(xpModel.report["final costs"][0])

        mmr = max_model.report
        udppr = udpp_model_xp.report
        mFromUdpp = maxFromUDPP.report
        omr = xpModel.report
        offer = xpModel.offers

        simulations = simulations.append(pd.Series([i, "total", num_flights, mmr["initial costs"][0],
                                          mmr["final costs"][0], udppr["final costs"][0],mFromUdpp["final costs"][0],
                                         omr["final costs"][0], offer["offers"][0]], index=simulations. columns),
                                         ignore_index=True)

        for airline in mmr["airline"][1:]:
            air_num_flights = df[df["airline"] == airline].shape[0]
            simulations = simulations.append(pd.Series([i, airline, air_num_flights,
                                                        mmr[mmr["airline"] == airline]["initial costs"].values[0],
                                                        mmr[mmr["airline"] == airline]["final costs"].values[0],
                                                        udppr[udppr["airline"] == airline]["final costs"].values[0],
                                                        mFromUdpp[mFromUdpp["airline"] == airline]["final costs"].values[0],
                                                        omr[omr["airline"] == airline]["final costs"].values[0],
                                                        offer[offer["airline"] == airline]["offers"].values[0]],
                                                       index=simulations.columns),
                                             ignore_index=True)
    except:
        pass

print(simulations)
simulations.to_csv("../test_beacon.csv", index=False)