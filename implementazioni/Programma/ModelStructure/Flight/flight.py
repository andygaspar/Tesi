import numpy as np
from typing import List, Callable

from Programma.ModelStructure.Slot import slot as sl


class Flight:

    def __init__(self, line, airline, slots: List[sl.Slot]):

        self.slot = slots[line["slot"]]

        self.num = line["num"]

        self.newSlot = None

        self.name = line["flight"]

        self.airline = airline

        self.eta = line["eta"]

        self.eta_slot = len([slot for slot in slots if slot.time <= self.eta]) - 1

        self.gdp_arrival = line["gdp schedule"]

        self.new_arrival = None

        self.cost = line["cost"]

        self.costFun = None

        self.compatible_slots = self.compute_compatible_slots(slots)

        self.localNum = None

        # UDPP attributes ***************

        self.UDPPLocalSlot = None

        self.UDPPlocalSolution = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def set_num(self, i):
        self.num = i

    def set_local_num(self, i):
        self.localNum = i

    def set_cost_fun(self, costFun: Callable):
        self.costFun = costFun

    def compute_compatible_slots(self, slots: List[sl.Slot]):
        try:
            compatible_slots = []
            for slot in slots:
                if slot.time > self.eta:
                    compatible_slots.append(slot)
            if compatible_slots[0].index > 0:
                compatible_slots.insert(0, slots[compatible_slots[0].index-1])
            return compatible_slots
        except IndexError:
            raise IndexError("No available slot for flight ", self.name)
