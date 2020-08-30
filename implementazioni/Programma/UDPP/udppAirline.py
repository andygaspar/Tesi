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
        self.AUslots = np.array([flight.slot for flight in self.flights])

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

    def slot_range(self, k):
        return range(self.AUslots[k] + 1, self.AUslots[k+1])

    def eta_limit(self, flight: UDPPFlight):
        i = 0
        for slot in self.AUslots:
            if slot >= flight.eta_slot:
                return i
            i += 1

    def UDPPLocal(self):

        self.x = np.array([[self.m.add_var(var_type=BINARY) for j in self.slotIndexes] for i in self.flights])

        self.z = np.array([self.m.add_var(var_type=INTEGER) for i in self.flights])

        self.y = np.array([[self.m.add_var(var_type=BINARY) for j in self.slotIndexes] for i in self.flights])

        flight: UDPPFlight

        self.m += xsum(self.x[0, k] for k in range(self.num_flights)) == 1

        # slot constraint
        for j in self.slotIndexes:
            self.m += xsum(self.y[flight.localNum, j] for flight in self.flights) <= 1

        for k in range(self.num_flights - 1):
            self.m += xsum(self.x[flight.localNum, k] for flight in self.flights) <= 1

            self.m += xsum(self.y[flight.localNum, self.AUslots[k]] for flight in self.flights) == 0

            self.m += xsum(self.y[i, j] for i in range(k, self.num_flights) for j in range(self.AUslots[k])) <= \
                      xsum(self.x[i, kk] for i in range(k+1) for kk in range(k, self.num_flights))

            self.m += xsum(self.y[flight.localNum, j] for flight in self.flights for j in self.slot_range(k)) \
                      == self.z[k]

            self.m += xsum(self.y[flight.localNum, j] for flight in self.flights for j in range(self.AUslots[k])) <= \
                      xsum(self.x[i, j] for i in range(k) for j in range(k, self.num_flights))

            for i in range(k+1):
                self.m += (1 - xsum(self.x[flight.localNum, i] for flight in self.flights))*1000 \
                          >= self.z[k] - (k-i)

        # last slot
        self.m += xsum(self.x[flight.localNum, self.num_flights - 1] for flight in self.flights) == 1

        for flight in self.flights[1:]:
            # flight assignment
            self.m += xsum(self.y[flight.localNum, j] for j in range(flight.eta_slot, flight.slot)) + \
                      xsum(self.x[flight.localNum, k] for k in
                           range(self.eta_limit(flight), self.num_flights)) == 1

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

        #print(self.m.status)

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
            #print(flight, xsol, ysol, "     ", flight.cost, flight.eta_slot)

            # if ysol not in [flight.slot for flight in self.flights] and ysol != "*":
            # print("******************************************** !!!!!!")
            # print(ysol, "    ", [flight.slot for flight in self.flights])
        # print(self.flights)
        # for flight in self.flights:
        #     print(flight, flight.slot, flight.UDPPsolution)



