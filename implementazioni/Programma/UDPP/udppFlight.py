from Programma.ModelStructure.Flight.flight import Flight


class UDPPFlight(Flight):

    def __init__(self, line, airline, model):
        super().__init__(line, airline, model)

        self.localNum = None

        self.UDPPLocalSlot = None

        self.UDPPsolution = None

    def set_local_num(self, i):
        self.localNum = i
