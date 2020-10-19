from Programma.ModelStructure.Slot.slot import Slot
import numpy as np
import pandas as pd


def make_slots_list(df: pd.DataFrame):
    slots = []
    slotIndexes = df["slot"].to_numpy()

    gdp_schedule = df["gdp schedule"].to_numpy()

    for i in range(len(slotIndexes)):
        slots.append(Slot(i, gdp_schedule[i]))

    return np.array(slots)
