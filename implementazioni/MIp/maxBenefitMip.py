from typing import Callable

from Programma.ModelStructure import modelStructure as mS
from mip import *
from Programma.ModelStructure.Airline import airline as air
from Programma.ModelStructure.Flight import flight as modFl
from Programma.ModelStructure.Solution import solution
from Programma.ModelStructure.Slot.slot import Slot

import numpy as np
import pandas as pd

import time


class MaxBenefitModel(mS.ModelStructure):

    def __init__(self, df_init: pd.DataFrame, costFun: Union[Callable, List[Callable]], model_name="Max Benefit"):

        self.airlineConstructor = air.Airline
        self.flightConstructor = modFl.Flight
        super().__init__(df_init=df_init, costFun=costFun)

        self.m = Model(model_name)
        self.x = None
        self.m.threads = -1
        self.m.verbose = 0
        self.mipSolution = None

    def set_variables(self):
        flight: modFl.Flight
        airline: air.Airline
        self.x = np.array([[self.m.add_var(var_type=BINARY) for k in self.slots] for flight in self.flights])

    def set_constraints(self):
        flight: modFl.Flight
        airline: air.Airline
        for flight in self.flights:
            self.m += xsum(self.x[flight.num, slot.index] for slot in flight.compatibleSlots) == 1

        for slot in self.slots:
            self.m += xsum(self.x[flight.num, slot.index] for flight in self.flights) <= 1

        for airline in self.airlines:
            self.m += xsum(flight.costFun(flight, flight.slot) for flight in airline.flights) >= \
                      xsum(self.x[flight.num, slot.index] * flight.costFun(flight, slot)
                           for flight in airline.flights for slot in self.slots)

    def set_objective(self):
        flight: modFl.Flight
        self.m.objective = minimize(
            xsum(self.x[flight.num, slot.index] * flight.costFun(flight, slot)
                 for flight in self.flights for slot in self.slots))

    def run(self):

        self.set_variables()

        start = time.time()
        self.set_constraints()
        end = time.time() - start
        #print("Constraints setting time ", end)

        self.set_objective()

        start = time.time()
        self.m.optimize()
        end = time.time() - start
        #print("Simplex time ", end)

        #print(self.m.status)

        mipSolution = self.x

        self.assign_flights(mipSolution)

        solution.make_solution(self)

        for flight in self.flights:
            if flight.eta > flight.newSlot.time:
                print("********************** danno *********************************",
                      flight, flight.eta, flight.newSlot.time)

    def assign_flights(self, mipSolution):
        for flight in self.flights:
            for slot in self.slots:
                if mipSolution[flight.slot.index, slot.index].x != 0:
                    flight.newSlot = slot
