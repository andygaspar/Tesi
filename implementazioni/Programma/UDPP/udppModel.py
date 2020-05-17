import numpy as np
import pandas as pd
from Programma.ModelStructure.modelStructure import ModelStructure
from Programma.UDPP.udppAirline import UDPPAirline
from Programma.UDPP.udppFlight import UDPPFlight
from Programma.ModelStructure.Solution import solution


class UDPPModel(ModelStructure):

    def __init__(self, df_init, cost_kind="quadratic"):

        self.airlineConstructor = UDPPAirline
        self.flightConstructor = UDPPFlight
        super().__init__(df_init=df_init, cost_kind=cost_kind)

        airline: UDPPAirline
        for airline in self.airlines:
            airline.setLocalFlightList(self.flights)
            airline.UDPPLocal_1()

        flight: UDPPFlight
        df_UDPP: pd.DataFrame
        UDPP_solution = [flight.UDPPsolution for flight in self.flights]
        self.df["UDPPpremerge"] = UDPP_solution
        df_UDPP = self.df.sort_values(by=["UDPPpremerge", "eta"])

        for i in range(df_UDPP.shape[0]):
            line = df_UDPP.iloc[i]
            flight = self.get_flight_name(line["flight"])
            if i < flight.eta_slot:
                print("************************************", flight, i, " earlier than eta")
            flight.new_slot = i
            flight.new_arrival = self.gdp_schedule[i]

        solution.make_solution(self, udpp=True)

    def get_new_df(self):
        self.df: pd.DataFrame
        self.df.reset_index(drop=True, inplace=True)
        self.df["slot"] = self.df["new slot"]
        self.df["gdp schedule"] = self.df["new arrival"]
        return self.df
