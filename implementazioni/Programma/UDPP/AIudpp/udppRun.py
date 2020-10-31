import numpy as np
from Programma.UDPP.AirlineAndFlightAndSlot.udppAirline import UDPPairline
from Programma.UDPP.Local.udppLocal import udpp_local


def run_UDPP_local(prior: np.array, air: UDPPairline, slots):
    for i in range(air.numFlights):
        air.flights[i].priorityNumber = prior[i]
    udpp_local(air, slots)