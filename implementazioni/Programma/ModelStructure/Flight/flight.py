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

        self.etaSlot = slots[len([slot for slot in slots if slot.time <= self.eta]) - 1]

        self.fpfs = line['fpfs']

        self.cost = line["cost"]

        try:
            self.margin = line["margins"]
        except:
            self.margin = None

        self.costFun = None

        self.compatibleSlots = self.compute_compatible_slots(slots)

        self.notCompatibleSlots = self.compute_not_compatible_slots(slots)

        self.localNum = None

        # UDPP attributes ***************

        self.UDPPLocalSlot = None

        self.UDPPlocalSolution = None

        # ISTOP attributes  *************

        self.priority = line["priority"]

        self.preference = None

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

    def delay(self, slot: sl.Slot):
        return slot.time - self.eta

    def compute_compatible_slots(self, slots: List[sl.Slot]):
        try:
            compatible_slots = []
            for slot in slots:
                if slot.time > self.eta:
                    compatible_slots.append(slot)
            if compatible_slots[0].index > 0:
                compatible_slots.insert(0, slots[compatible_slots[0].index - 1])
            return compatible_slots
        except IndexError:
            raise IndexError("No available slot for flight ", self.name)

    def compute_not_compatible_slots(self, slots):
        notCompatibleSlots = []
        for slot in slots:
            if slot not in self.compatibleSlots:
                notCompatibleSlots.append(slot)
        return notCompatibleSlots
