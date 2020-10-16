from Programma.ModelStructure.modelStructure import ModelStructure
from Programma.ModelStructure.Flight.flight import Flight


def cost_function(model: ModelStructure, flight: Flight, j):
    if model.cost_kind == "linear":
        return flight.cost * model.delays[flight.num, j]

    if model.cost_kind == "quadratic":
        return (flight.cost * (model.delays[flight.num, j]) ** 2)/2