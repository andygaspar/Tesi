

class Slot:

    def __init__(self, index: int, time: int):

        self.index = index
        self.time = time
        # self.flight = flight

    def __str__(self):
        return str(self.index)

    def __repr__(self):
        return str(self.time)