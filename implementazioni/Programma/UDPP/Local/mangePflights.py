from typing import Union, Callable, List

from Programma.UDPP.AirlineAndFlightAndSlot.udppFlight import UDPPflight
from Programma.UDPP.AirlineAndFlightAndSlot.udppAirline import UDPPairline
from Programma.UDPP.AirlineAndFlightAndSlot.udppSlot import UDPPslot
from Programma.ModelStructure.modelStructure import ModelStructure
from Programma.ModelStructure.Solution import solution
import numpy as np


def get_target_slot(targetTime, slotList: List[UDPPslot]):
    if targetTime < slotList[0].time:
        return UDPPslot.is_null()

    for i in range(len(slotList) - 1):
        if slotList[i].time <= targetTime < slotList[i + 1].time:
            return slotList[i]
    return slotList[-1]


def get_first_later_free_slot(targetSlot: UDPPslot, slotList: List[UDPPslot]):
    for slot in slotList[targetSlot.localIndex:]:
        if slot.free:
            return slot


def sort_flights_by_tna(flights):
    tnaList = [f.tna for f in flights]
    sorted_indexes = np.flip(np.argsort(tnaList))
    return np.array([flights[i] for i in sorted_indexes])


def sort_slots_by_time(slotList):
    timeList = [slot.time for slot in slotList]
    sorted_indexes = np.flip(np.argsort(timeList))
    return np.array([slotList[i] for i in sorted_indexes])


def sort_Pflights(Pflights):
    pfSorted = sort_flights_by_tna(Pflights)
    slotSorted = sort_slots_by_time([pf.newSlot for pf in Pflights])
    for i in range(len(Pflights)):
        pfSorted[i].newSlot = slotSorted[i]
    for pf in Pflights:
        if pf.newSlot.time < pf.eta:
            print("problem in Pflights sorting")


def manage_Pflights(Pflights: List[UDPPflight], localSlots: List[UDPPslot], slots: List[UDPPslot]):

    for pf in Pflights:
        targetSlot = get_target_slot(pf.tna, localSlots)

        if targetSlot.is_null():
            targetSlot = get_first_later_free_slot(localSlots[0], localSlots)

        if targetSlot.time >= pf.tnb:
            pf.assign(targetSlot)
        else:
            if pf.tnb >= pf.eta:
                pf.assign(get_target_slot(pf.tnb, slots))
            else:
                pf.assign(get_target_slot(pf.eta, slots))

        localSlots.remove(targetSlot)
        
    sort_Pflights(Pflights)
