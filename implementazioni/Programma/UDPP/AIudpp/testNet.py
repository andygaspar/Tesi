import random

import matplotlib.pyplot as plt

import numpy as np
import torch
from torch import nn, optim
from IPython import display

from Programma.UDPP import udppModel
from Programma.UDPP.AirlineAndFlightAndSlot.udppAirline import UDPPairline
from Programma.UDPP.AirlineAndFlightAndSlot.udppSlot import UDPPslot
from data.dfMaker import df_maker
from Programma.ModelStructure.modelStructure import ModelStructure
from Programma.ModelStructure.Costs.costFunctionDict import CostFuns
from Programma.UDPP.Local.manageMflights import manage_Mflights

airline: UDPPairline

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

df = df_maker(custom=[6, 4, 3, 7, 2, 8])
costFun = CostFuns().costFun["linear"]
mod = ModelStructure(df, costFun)
df["margins"] = [random.choice(range(10, 50)) for i in range(df.shape[0])]

udMod = udppModel.UDPPModelOpt(df, costFun)
airline = [air for air in udMod.airlines if air.name == "A"][0]



print(airline)
print([f.priorityNumber for f in airline.flights])
vals = [[f.tna, f.eta, f.slot.time, f.cost] for f in airline.flights]
X = torch.tensor([item for val in vals for item in val]).to(device).reshape(1, 24).type(dtype=torch.float32)
print(X)


lr = 1e-3
lambdaL2 = 1e-5
epochs = 1000

model = nn.Sequential(
    nn.Linear(24, 64),
    nn.ReLU(),
    nn.Linear(64, 6))
model.to(device)

with torch.no_grad():
    priorities = model(X).flatten().cpu().numpy()

for i in range(airline.numFlights):
    airline.flights[i].priorityNumber = priorities[i]

slotList = [UDPPslot(flight.slot, flight, flight.localNum) for flight in airline.flights if flight.priority != "B"]
manage_Mflights(airline.flights, slotList)

print([f.priorityNumber for f in airline.flights])

criterion = nn.CrossEntropyLoss()

optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=lambdaL2)

torch.manual_seed(41)
N = 1000  # num_samples_per_class
D = 2  # dimensions
C = 3  # num_classes
H = 100  # num_hidden_units

X = torch.zeros(N * C, D).to(device)
y = torch.zeros(N * C, dtype=torch.long).to(device)
print(torch.cuda.is_available())

# for c in range(C):
#     index = 0
#     t = torch.linspace(0, 1, N)
#     # When c = 0 and t = 0: start of linspace
#     # When c = 0 and t = 1: end of linpace
#     # This inner_var is for the formula inside sin() and cos() like sin(inner_var) and cos(inner_Var)
#     inner_var = torch.linspace(
#         # When t = 0
#         (2 * np.pi / C) * (c),
#         # When t = 1
#         (2 * np.pi / C) * (2 + c),
#         N
#     ) + torch.randn(N) * 0.2
#
#     for ix in range(N * c, N * (c + 1)):
#         X[ix] = t[index] * torch.FloatTensor((
#             np.sin(inner_var[index]), np.cos(inner_var[index])
#         ))
#         y[ix] = c
#         index += 1



print("Shapes:")
print("X:", X.size())
print("y:", y.size())


# for e in range(epochs):
#     y_pred = model(X)
#     loss = criterion(y_pred, y)
#     print("[EPOCH]: {}, [LOSS]: {}".format(e, loss.item()))
#     display.clear_output(wait=True)
#
#     optimizer.zero_grad()
#     loss.backward()
#     optimizer.step()
