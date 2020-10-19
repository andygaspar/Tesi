from Programma.ModelStructure.Flight.flight import Flight


class Slot:

    def __init__(self, index: int, time: int, flight: Flight = None):

        self.index = index
        self.time = time
        self.flight = flight
