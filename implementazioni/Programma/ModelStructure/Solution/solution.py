import numpy as np
import pandas as pd


def make_solution_array(model):
    from Programma.ModelStructure.modelStructure import ModelStructure
    from Programma.ModelStructure.Flight.flight import Flight
    model: ModelStructure
    flight: Flight

    solution_array = np.zeros((model.slots.shape[0], model.slots.shape[0]))
    for flight in model.flights:
        for j in range(len(model.mipSolution[flight.num])):
            solution_array[flight.slot.index, j] = model.mipSolution[flight.num][j].x
    model.solutionArray = solution_array


def update_flights(model):
    from Programma.ModelStructure.modelStructure import ModelStructure
    from Programma.ModelStructure.Flight.flight import Flight
    model: ModelStructure
    flight: Flight

    for flight in model.flights:
        flight.newSlot = np.argwhere(model.solutionArray[flight.num])[0][0]
        flight.new_arrival = model.slotTimeGrid[flight.newSlot]


def make_performance_df(model):
    from Programma.ModelStructure.modelStructure import ModelStructure
    from Programma.ModelStructure.Airline.airline import Airline
    from Programma.ModelStructure.Flight.flight import Flight
    model: ModelStructure
    airline: Airline
    flight: Flight
    airline_names = ["total"] + [airline.name for airline in model.airlines]
    initial_costs = [model.initialTotalCosts]
    final_costs = [model.compute_costs(model.flights, "final")]
    for airline in model.airlines:
        initial_costs.append(model.compute_costs(airline.flights, "initial"))
        final_costs.append(model.compute_costs(airline.flights, "final"))

    model.report = pd.DataFrame(
        {"airline": airline_names, "initial costs": initial_costs, "final costs": final_costs})


def make_df_solution(model, udpp):
    from Programma.ModelStructure.modelStructure import ModelStructure
    model: ModelStructure
    # if udpp == False:
    #     make_solution_array(model)
    #     update_flights(model)

    new_slot = [flight.newSlot.index for flight in model.flights]
    new_arrival = [flight.new_arrival for flight in model.flights]
    eta_slot = [flight.eta_slot for flight in model.flights]
    model.df["new slot"] = new_slot
    model.df["new arrival"] = new_arrival
    model.df["eta slot"] = eta_slot
    model.df.sort_values(by="new slot", inplace=True)


def make_solution(model, udpp=False):
    from Programma.ModelStructure.modelStructure import ModelStructure
    model: ModelStructure
    make_df_solution(model, udpp)
    make_performance_df(model)
    #print(model.df)
    print(model.report)
