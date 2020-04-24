import numpy as np
from Programma.Airline import airline as air


def make_airlines_list(model):
    airline_list = []
    airline_index = 0
    for airline in model.df["airline"].unique():
        if airline != "Empty":
            airline_list.append(air.Airline(model.df[model.df["airline"] == airline], airline_index, model))
            airline_index += 1
    return np.array(airline_list)
