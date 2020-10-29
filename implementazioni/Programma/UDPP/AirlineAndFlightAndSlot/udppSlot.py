from Programma.ModelStructure.Slot.slot import Slot
from Programma.UDPP.AirlineAndFlightAndSlot.udppFlight import UDPPflight


class UDPPslot(Slot):

    def __init__(self, slot: Slot, flight: UDPPflight = None, localIndex: int = None):

        super().__init__(slot.index, slot.time)
        self.localIndex = localIndex
        self.flight = flight
        self.free = True
        self.isNull = False
        self.shiftBlocked = False

    @staticmethod
    def shift_blocked():
        sb = UDPPslot(Slot(None, None))
        sb.shiftBlocked = True

    @staticmethod
    def is_null():
        null = UDPPslot(Slot(None, None))
        null.isNull = True
