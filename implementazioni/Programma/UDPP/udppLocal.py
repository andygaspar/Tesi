from mip import *
import numpy as np
from Programma.ModelStructure.Airline import airline as air
from Programma.ModelStructure.Flight import flight as fl
from Programma.ModelStructure.Slot import slot as sl

# def costo_provvisorio(f):
#     return (f.cost * (f.slot.time - f.eta) ** 2) / 2


# def costo_provvisorio_finale(f):
#     return (f.cost * (f.UDPPlocalSolution.time - f.eta) ** 2) / 2


def slot_range(k: int, AUslots: List[sl.Slot]):
    return range(AUslots[k].index + 1, AUslots[k + 1].index)


def eta_limit_slot(flight: fl.Flight, AUslots: List[sl.Slot]):
    i = 0
    for slot in AUslots:
        if slot >= flight.etaSlot:
            return i
        i += 1


def UDPPlocal(airline: air.Airline, slots: List[sl.Slot]):
    m = Model(name)
    m.threads = -1
    m.verbose = 0

    x = np.array([[m.add_var(var_type=BINARY) for j in slots] for i in airline.flights])

    z = np.array([m.add_var(var_type=INTEGER) for i in airline.flights])

    y = np.array([[m.add_var(var_type=BINARY) for j in slots] for i in airline.flights])

    flight: fl.Flight

    m += xsum(x[0, k] for k in range(airline.numFlights)) == 1

    # slot constraint
    for j in slots:
        m += xsum(y[flight.localNum, j.index] for flight in airline.flights) <= 1

    for k in range(airline.numFlights - 1):
        m += xsum(x[flight.localNum, k] for flight in airline.flights) <= 1

        m += xsum(y[flight.localNum, airline.AUslots[k].index] for flight in airline.flights) == 0

        m += xsum(y[i, j] for i in range(k, airline.numFlights) for j in range(airline.AUslots[k].index)) <= \
             xsum(x[i, kk] for i in range(k + 1) for kk in range(k, airline.numFlights))

        m += xsum(y[flight.localNum, j] for flight in airline.flights for j in slot_range(k, airline.AUslots)) \
             == z[k]

        m += xsum(
            y[flight.localNum, j] for flight in airline.flights for j in range(airline.AUslots[k].index)) <= \
             xsum(x[i, j] for i in range(k) for j in range(k, airline.numFlights))

        for i in range(k + 1):
            m += (1 - xsum(x[flight.localNum, i] for flight in airline.flights)) * 1000 \
                 >= z[k] - (k - i)

    # last slot
    m += xsum(x[flight.localNum, airline.numFlights - 1] for flight in airline.flights) == 1

    for flight in airline.flights[1:]:
        # flight assignment
        m += xsum(y[flight.localNum, j] for j in range(flight.etaSlot.index, flight.slot.index)) + \
             xsum(x[flight.localNum, k] for k in
                  range(eta_limit_slot(flight, airline.AUslots), airline.numFlights)) == 1

    # not earlier than its first flight
    m += xsum(
        y[flight.localNum, j] for flight in airline.flights for j in range(airline.flights[0].slot.index)) == 0

    m.objective = minimize(
        xsum(y[flight.localNum][slot.index] * flight.costFun(flight, slot)
             for flight in airline.flights for slot in slots) +
        xsum(x[flight.localNum][k] * flight.costFun(flight, airline.AUslots[k])
             for flight in airline.flights for k in range(airline.numFlights)))

    m.optimize()

    # print(m.status)

    protection = False
    for flight in airline.flights:
        xsol = "*"
        ysol = "*"

        for k in range(airline.numFlights):
            if x[flight.localNum, k].x != 0:
                xsol = airline.flights[k].slot
                flight.UDPPlocalSolution = airline.flights[k].slot

        for slot in slots:
            if y[flight.localNum, slot.index].x != 0:
                ysol = slots[j.index]
                flight.UDPPlocalSolution = slot
                # print("**************************")
                protection = True
        # print(flight, xsol, ysol, "     ", flight.cost, flight.eta_slot)

        # if ysol not in [flight.slot for flight in flights] and ysol != "*":
        # print("******************************************** !!!!!!")
        # print(ysol, "    ", [flight.slot for flight in flights])

    # if sum([costo_provvisorio(f) for f in airline.flights]) < sum([costo_provvisorio_finale(f) for f in airline.flights]):
    #     print("\n\nPROBLEMA           MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM")
    #     print(airline, sum([costo_provvisorio(f) for f in airline.flights]), sum([costo_provvisorio_finale(f) for f in airline.flights]))
    #     for f in airline.flights:
    #         print(f.slot.time, f.UDPPlocalSolution.time, f.cost, f.eta)
    #
    # if protection == True:
    #     for f in airline.flights:
    #         print(f.slot.time, f.UDPPlocalSolution.time, f.cost, f.eta)
