import numpy as np


class Flight:

    def __init__(self, init_slot, name, airline, eta, schedule, priority, comp_slots, not_comp_slots, cost=None):
        self.slot = init_slot
        self.name = name
        self.airline = airline
        self.eta = eta
        self.schedule = schedule
        self.cost = cost
        self.compatible_slots = comp_slots
        self.not_compatible_slots = not_comp_slots
        self.priority = priority
        self.preference = None

    def set_preference(self, num_flights, sum_priorities, f):
        self.preference = f(self.priority, num_flights) / sum_priorities

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
