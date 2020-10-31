import random

import matplotlib.pyplot as plt

import numpy as np
from IPython import display
import torch.tensor

from Programma.UDPP import udppModel
from Programma.UDPP.AirlineAndFlightAndSlot.udppAirline import UDPPairline
from Programma.UDPP.AirlineAndFlightAndSlot.udppSlot import UDPPslot
from data.dfMaker import df_maker
from Programma.ModelStructure.modelStructure import ModelStructure
from Programma.ModelStructure.Costs.costFunctionDict import CostFuns
from Programma.UDPP.Local.udppLocal import udpp_local
from Programma.UDPP.AIudpp import network as nn


airline: UDPPairline




def make_network_input(airline):
    vals = [[f.tna, f.eta, f.slot.time, f.cost] for f in airline.flights]
    return [item for val in vals for item in val]


def run_UDPP_local(priorities, airline, slots):

    for i in range(airline.numFlights):
        airline.flights[i].priorityNumber = priorities[i]
    udpp_local(airline, slots)


net = nn.AirNetwork()


df = df_maker(custom=[6, 4, 3, 7, 2, 8])
costFun = CostFuns().costFun["linear"]
mod = ModelStructure(df, costFun)
df["margins"] = [random.choice(range(10, 50)) for i in range(df.shape[0])]

udMod = udppModel.UDPPModelOpt(df, costFun)
airline = [air for air in udMod.airlines if air.name == "A"][0]


inputs = []

for i in range(3):

    initialCost = udMod.compute_costs(airline.flights, "initial")
    inputVect = make_network_input(airline)
    priorities = net.prioritisation(inputVect)
    inputs.append(inputVect)

    run_UDPP_local(priorities, airline, udMod.slots)

    finalCost = udMod.compute_costs(airline.flights, "final")

    print(initialCost, finalCost)


x = torch.tensor(inputs)
print(x.shape)

print(net.prioritisation(x).shape)