import random

import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
from IPython import display
import torch.tensor

from Programma.UDPP import udppModel
from Programma.UDPP.AIudpp.udppRun import run_UDPP_local
from Programma.UDPP.AirlineAndFlightAndSlot.udppAirline import UDPPairline as Airline
from Programma.UDPP.AirlineAndFlightAndSlot.udppSlot import UDPPslot
from data.dfMaker import df_maker
from Programma.ModelStructure.modelStructure import ModelStructure
from Programma.ModelStructure.Costs.costFunctionDict import CostFuns
from Programma.UDPP.AIudpp import network as nn


def make_network_input(air: Airline):
    vals = [[f.tna, f.eta, f.slot.time, f.cost] for f in air.flights]
    return [item for val in vals for item in val]




airline: Airline

batchSize = 40

net = nn.AirNetwork(24, batchSize)

inputs = []
initialCosts = []
finalCosts = []
airlines = []
UDPPmodels = []

for run in range(batchSize):
    df = df_maker(custom=[6, 4, 3, 7, 2, 8])
    df["margins"] = [random.choice(range(10, 50)) for i in range(df.shape[0])]
    # df.to_csv("crash")
    # df = pd.read_csv("crash")
    costFun = CostFuns().costFun["linear"]
    # mod = ModelStructure(df, costFun)

    udMod = udppModel.UDPPmodel(df, costFun)
    UDPPmodels.append(udMod)

    airline = [air for air in udMod.airlines if air.name == "A"][0]
    airlines.append(airline)

    initialCosts.append(udMod.compute_costs(airline.flights, "initial"))

    inputVect = make_network_input(airline)
    # priorities = net.prioritisation(inputVect)
    inputs.append(inputVect)

    # run_UDPP_local(priorities, airline, udMod.slots)

    # finalCosts.append(udMod.compute_costs(airline.flights, "final"))

net.train(6, batchSize, inputs, np.array(initialCosts), airlines, UDPPmodels)
