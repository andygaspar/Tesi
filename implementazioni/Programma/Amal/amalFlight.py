import numpy as np
from Programma.Flight import flight as fl


class AmalFlight(fl.Flight):

    def __init__(self, line, airline, model):

        super().__init__(line, airline, model)

        self.priority = line["priority"]

        self.currentDelay = self.gdp_arrival - self.eta





