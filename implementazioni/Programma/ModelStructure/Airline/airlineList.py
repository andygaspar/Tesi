import numpy as np
import pandas as pd
from typing import List

from Programma.ModelStructure.Slot import slot
from Programma.ModelStructure.Airline import airline as air


def make_airlines_list(df: pd.DataFrame, slots: List[slot.Slot]):
    airline_list = []
    airline_index = 0
    for airline in df["airline"].unique():
        if airline != "Empty":
            airline_list.append(
                air.Airline(df[df["airline"] == airline], airline_index, slots))
            airline_index += 1
    return np.array(airline_list)
