from Programma.ModelStructure.modelStructure import ModelStructure
from Programma.ModelStructure.Flight.flight import Flight


def cost_function(model: ModelStructure, flight: Flight, slot):
    if model.cost_kind == "linear":
        return flight.cost * model.delays[flight.num, slot.index]

    if model.cost_kind == "quadratic":
        return (flight.cost * (model.delays[flight.num, slot.index]) ** 2)/2