import numpy as np


def sort_flights_by_time(flights):
    time_list = [f.UDPPlocalSolution.time for f in flights]
    sorted_indexes = np.argsort(time_list)
    return np.array([flights[i] for i in sorted_indexes])


def UDPPmerge(flights, slots):
    sorted_flights = sort_flights_by_time(flights)
    i = 0
    for f in sorted_flights:
        f.newSlot = slots[i]
        i += 1
