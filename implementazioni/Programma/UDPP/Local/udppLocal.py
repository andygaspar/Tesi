from typing import Union, Callable, List

from Programma.UDPP.AirlineAndFlightAndSlot.udppFlight import UDPPflight
from Programma.UDPP.AirlineAndFlightAndSlot.udppAirline import UDPPairline
from Programma.ModelStructure.Slot.slot import Slot
from Programma.UDPP.AirlineAndFlightAndSlot.udppSlot import UDPPslot
from Programma.ModelStructure.modelStructure import ModelStructure
from Programma.ModelStructure.Solution import solution
from Programma.UDPP.Local.manageMflights import manage_Mflights


def make_slot_list(flights: List[UDPPflight]):
    return [flight for flight in flights if flight.priority != "B"]


def manage_Pflights(Pflights, slotList):
    pass


def udpp_local(airline: UDPPairline, slots: List[Slot]):

    slotList: List[UDPPslot]
    Pflights: List[UDPPflight]
    Mflights: List[UDPPflight]

    slotList = [UDPPslot(flight.slot, flight, flight.localNum) for flight in airline.flights if flight.priority != "B"]
    Pflights = [flight for flight in airline.flights if flight.priority != "P"]
    manage_Pflights(Pflights, slotList)

    Mflights = [flight for flight in airline.flights if flight.priority != "P"]
    manage_Mflights(Mflights, slotList)

    for flight in airline.flights:
        flight.UDPPlocalSolution = flight.newSlot

