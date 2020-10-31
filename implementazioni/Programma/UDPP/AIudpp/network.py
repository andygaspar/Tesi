import random
from typing import List

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


class AirNetwork:

    def __init__(self, inputDimension, batchSize):

        self.inputDimension = inputDimension
        self.batchSize = batchSize
        lr = 1e-3
        lambdaL2 = 1e-5
        epochs = 1000

        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        self.network = nn.Sequential(
            nn.Linear(self.inputDimension, 64),
            nn.ReLU(),
            nn.Linear(64, 6))
        self.network.to(self.device)

        torch.cuda.current_device()
        print(torch.cuda.is_available())
        self.optimizer = optim.Adam(self.network.parameters(), lr=1e-5, weight_decay=1e-5)

    def prioritisation(self, input_list: List[float]):

        X = torch.tensor(input_list, requires_grad=True).to(self.device).reshape(1, self.inputDimension).type(dtype=torch.float32)

        with torch.no_grad():
            priorities = self.network(X).flatten().cpu().numpy()

        return priorities

    def train(self, inputs, initialCosts: np.array, finalCosts: np.array):
        X = torch.tensor(inputs).to(self.device)\
            .reshape(self.batchSize, self.inputDimension).type(dtype=torch.float32)

        with torch.no_grad():
            Y = self.network(X)

        priorities = Y.flatten().cpu().numpy()

        loss = self.averageReduction(initialCosts, finalCosts)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    @staticmethod
    def averageReduction(initialCosts, finalCosts):
        return torch.tensor(initialCosts-finalCosts)

# criterion = nn.CrossEntropyLoss()
#
# optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=lambdaL2)
#
# torch.manual_seed(41)
# N = 1000  # num_samples_per_class
# D = 2  # dimensions
# C = 3  # num_classes
# H = 100  # num_hidden_units
#
# X = torch.zeros(N * C, D).to(device)
# y = torch.zeros(N * C, dtype=torch.long).to(device)
# print(torch.cuda.is_available())
#
# # for c in range(C):
# #     index = 0
# #     t = torch.linspace(0, 1, N)
# #     # When c = 0 and t = 0: start of linspace
# #     # When c = 0 and t = 1: end of linpace
# #     # This inner_var is for the formula inside sin() and cos() like sin(inner_var) and cos(inner_Var)
# #     inner_var = torch.linspace(
# #         # When t = 0
# #         (2 * np.pi / C) * (c),
# #         # When t = 1
# #         (2 * np.pi / C) * (2 + c),
# #         N
# #     ) + torch.randn(N) * 0.2
# #
# #     for ix in range(N * c, N * (c + 1)):
# #         X[ix] = t[index] * torch.FloatTensor((
# #             np.sin(inner_var[index]), np.cos(inner_var[index])
# #         ))
# #         y[ix] = c
# #         index += 1
#
#
# print("Shapes:")
# print("X:", X.size())
# print("y:", y.size())
#
# # for e in range(epochs):
# #     y_pred = model(X)
# #     loss = criterion(y_pred, y)
# #     print("[EPOCH]: {}, [LOSS]: {}".format(e, loss.item()))
# #     display.clear_output(wait=True)
# #
# #     optimizer.zero_grad()
# #     loss.backward()
#     optimizer.step()