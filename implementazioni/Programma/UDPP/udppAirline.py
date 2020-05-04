import numpy as np
import pandas as pd
import copy
from Programma.UDPP.udppFlight import UDPPFlight
from Programma.ModelStructure.Airline.airline import Airline
from mip import *


class UDPPAirline(Airline):

    def __init__(self, df_airline: pd.DataFrame, airline_index, model):
        super().__init__(df_airline, airline_index, model)

        self.model = model

        self.modelFlightList = None
        self.slotIndexes = model.slotIndexes

        self.m = self.m = Model(self.name)
        self.x = None
        self.y = None
        self.z = None
        self.m.threads = -1
        self.m.verbose = 0

        for i in range(len(self.flights)):
            self.flights[i].set_local_num(i)

    def setLocalFlightList(self, flight_list):

        self.modelFlightList = flight_list

    def UDPPLocal(self):

        self.x = np.array([[self.m.add_var(var_type=BINARY) for j in self.slotIndexes] for i in self.flights])

        self.y = np.array([[self.m.add_var(var_type=BINARY) for j in self.slotIndexes] for i in self.flights])

        flight: UDPPFlight

        self.m += xsum(self.x[0, k] for k in range(self.num_flights)) == 1

        # slot constraint
        for k in range(self.num_flights - 1):
            self.m += xsum(self.x[flight.localNum, k] for flight in self.flights) + \
                      xsum(self.y[flight.localNum, j] for flight in self.flights
                           for j in range(self.flights[k].slot, self.flights[k + 1].slot)) \
                      <= 1

        # last slot
        self.m += xsum(self.x[flight.localNum, self.num_flights - 1] for flight in self.flights) == 1

        for flight in self.flights[1:]:
            # flight assignment
            self.m += xsum(self.y[flight.localNum, j] for j in range(flight.eta_slot, flight.slot)) + \
                      xsum(self.x[flight.localNum, k] for k in range(flight.localNum, self.num_flights)) == 1

        # not earlier than its first flight
        self.m += xsum(self.y[flight.localNum, j] for flight in self.flights for j in range(self.flights[0].slot)) == 0

        from Programma.ModelStructure.modelStructure import ModelStructure
        self.model: ModelStructure

        self.m.objective = minimize(
            xsum(self.y[flight.localNum][j] * self.model.cost_function(flight, j)
                 for flight in self.flights for j in self.slotIndexes) +
            xsum(self.x[flight.localNum][k] * self.model.cost_function(flight, self.flights[k].num)
                 for flight in self.flights for k in range(self.num_flights)))

        self.m.optimize()

        # print(self.m.status)

        for flight in self.flights:
            xsol = "*"
            ysol = "*"

            for k in range(self.num_flights):
                if self.x[flight.localNum, k].x != 0:
                    xsol = self.flights[k].slot
                    flight.UDPPsolution = self.flights[k].slot

            for j in self.slotIndexes:
                if self.y[flight.localNum, j].x != 0:
                    ysol = self.slotIndexes[j]
                    flight.UDPPsolution = self.slotIndexes[j]
            # print(flight, flight.slot, xsol, ysol)

            # if ysol not in [flight.slot for flight in self.flights] and ysol != "*":
                # print("******************************************** !!!!!!")
                # print(ysol, "    ", [flight.slot for flight in self.flights])

        # print("\n\n*****")
