from typing import Union, Callable, List

from Programma.UDPP.AirlineAndFlightAndSlot.udppFlight import UDPPflight
from Programma.UDPP.AirlineAndFlightAndSlot.udppAirline import UDPPairline
from Programma.UDPP.AirlineAndFlightAndSlot.udppSlot import UDPPslot
from Programma.ModelStructure.modelStructure import ModelStructure
from Programma.ModelStructure.Solution import solution
import numpy as np


def sort_flights_by_priority(flights):
    time_list = [f.priorityNumber for f in flights]
    sorted_indexes = np.argsort(time_list)
    return np.array([flights[i] for i in sorted_indexes])


def get_target_slot(targetTime, slotList: List[UDPPslot]):
    if targetTime <= slotList[0].time:
        return UDPPslot.is_null()

    for i in range(len(slotList) - 1):
        if slotList[i].time <= targetTime < slotList[i + 1].time:
            return slotList[i]
    return slotList[-1]


def available_free_slot_at_or_earlier(targetSlot: UDPPslot, slotList: List[UDPPslot]):
    for i in range(len(slotList) - 1):
        if slotList[i] <= targetSlot and slotList[i].free:
            return True
    return False


def move_flight_earlier(targetSlot: UDPPslot, flight: UDPPflight, slotList: List[UDPPslot]):
    fromSlot = targetSlot
    toSlot = slotList[targetSlot.localIndex-1]
    while True:

        if flight.eta > fromSlot.time:
            return UDPPslot.shift_blocked()

        if fromSlot.free:
            return fromSlot

        if toSlot.isNull:
            return toSlot

        currentSlot = move_flight_earlier(toSlot, fromSlot.flight, slotList)

        if not currentSlot.isNull and not currentSlot.shiftBlocked:
            fromSlot.flight.assign(currentSlot)
            fromSlot.free = True

            return fromSlot

        if currentSlot.isNull:
            return currentSlot

        fromSlot = slotList[fromSlot.localIndex - 1]
        toSlot = slotList[fromSlot.localIndex - 1]


def manage_solution_earlier(targetSlot: UDPPslot, flight: UDPPflight, slotList: List[UDPPslot]):
    if not available_free_slot_at_or_earlier(targetSlot, slotList):
        return UDPPslot.is_null()

    else:
        for currentSlot in slotList[targetSlot.localIndex:]:
            solutionSlot = move_flight_earlier(currentSlot, flight, slotList)
            if solutionSlot:
                return solutionSlot


def get_first_later_free_slot(targetSlot: UDPPslot, slotList: List[UDPPslot]):
    for slot in slotList[targetSlot.localIndex:]:
        if slot.free:
            return slot


def manage_time_solution(targetTime, flight: UDPPflight, slotList: List[UDPPslot]):
    targetSlot = get_target_slot(targetTime, slotList)
    solutionSlot = manage_solution_earlier(targetSlot, flight, slotList)

    if solutionSlot.isNull:
        solutionSlot = get_first_later_free_slot(targetSlot, slotList)

    flight.assign(solutionSlot)


def manage_Mflights(Mflights: List[UDPPflight], slotList: List[UDPPslot]):
    Mflights = list(sort_flights_by_priority(Mflights))
    for mf in Mflights:
        manage_time_solution(mf.tna, mf, slotList)
