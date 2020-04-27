import numpy as np
import string
from scipy import stats
import pandas as pd


def avoid_zero(flight_list, num_flights):
    while len(flight_list[flight_list < 1]) > 0:
        for i in range(flight_list.shape[0]):
            if flight_list[i] == 0:
                flight_list[i] += 1
                if sum(flight_list) > num_flights:
                    flight_list[np.argmax(flight_list)] -= 1
    return flight_list


def fill_missing_flights(flight_list, num_flights, num_airlines):
    missing = num_flights - sum(flight_list)
    for i in range(missing):
        custm = stats.rv_discrete(name='custm', values=(np.arange(num_airlines), flight_list / sum(flight_list)))
        flight_list[custm.rvs(size=1)] += 1
    return np.flip(np.sort(flight_list))


def distribution_maker(num_flights, num_airlines, distribution="uniform"):
    dist = []

    if distribution == "uniform":
        h, loc = np.histogram(np.random.uniform(0, 1, 1000), bins=num_airlines)
        dist = ((np.flip(np.sort(h)) / sum(h)) * num_flights).astype(int)

    if distribution == "few_high_few_low":
        f = lambda x: x ** 3 + 1
        base = np.linspace(-1, 1, num_airlines)
        custm = stats.rv_discrete(name='custm', values=(np.arange(num_airlines), f(base) / sum(f(base))))
        h, loc = np.histogram(custm.rvs(size=1000), bins=num_airlines)
        dist = ((np.flip(np.sort(h)) / sum(h)) * num_flights).astype(int)

    if distribution == "few_low":
        f = lambda x: x ** 4 + 1
        base = np.linspace(-1, 1 / 4, num_airlines)
        custm = stats.rv_discrete(name='custm', values=(np.arange(num_airlines), f(base) / sum(f(base))))
        h, loc = np.histogram(custm.rvs(size=1000), bins=num_airlines)
        dist = ((np.flip(np.sort(h)) / sum(h)) * num_flights).astype(int)

    if distribution == "few_high":
        f = lambda x: x ** 2
        base = np.linspace(0, 1, num_airlines)
        val = f(base)
        val[val > 3 / 4] = 3 / 4
        custm = stats.rv_discrete(name='custm', values=(np.arange(num_airlines), val / sum(val)))
        h, l = np.histogram(custm.rvs(size=1000), bins=num_airlines)
        dist = ((np.flip(np.sort(h)) / sum(h)) * num_flights).astype(int)

    if distribution == "increasing":
        f = lambda x: x
        base = np.linspace(0, 1, num_airlines)
        custm = stats.rv_discrete(name='custm', values=(np.arange(num_airlines), f(base) / sum(f(base))))
        h, loc = np.histogram(custm.rvs(size=1000), bins=num_airlines)
        dist = ((np.flip(np.sort(h)) / sum(h)) * num_flights).astype(int)

    if distribution == "hub":
        f = lambda x: x ** 10
        base = np.linspace(0, 1, num_airlines)
        custm = stats.rv_discrete(name='custm', values=(np.arange(num_airlines), f(base) / sum(f(base))))
        h, loc = np.histogram(custm.rvs(size=1000), bins=num_airlines)
        dist = ((np.flip(np.sort(h)) / sum(h)) * num_flights).astype(int)

    dist = avoid_zero(dist, num_flights)
    dist = fill_missing_flights(dist, num_flights, num_airlines)
    return dist


def df_maker(num_flights=20, num_airlines=3, distribution="uniform", capacity=1, new_capacity=2):
    dist = distribution_maker(num_flights, num_airlines, distribution)
    airline = [[string.ascii_uppercase[j] for i in range(dist[j])] for j in range(num_airlines)]
    airline = [val for sublist in airline for val in sublist]
    airline = np.random.permutation(airline)
    flights = ["F" + airline[i] + str(i + 1) for i in range(num_flights)]

    slot = np.arange(num_flights)
    eta = slot * capacity
    gdp = slot * new_capacity
    priority = np.random.uniform(0.5, 2, num_flights)
    cost = priority

    return pd.DataFrame(
        {"slot": slot, "flight": flights, "eta": eta, "gdp schedule": gdp, "priority": priority, "airline": airline,
         "cost": cost})

