import numpy as np
import pandas as pd
from Programma.Amal.amalOffer import AmalOffer
from Programma.Amal import amalFlight as modFl
from Programma.Airline import airline as air


class AmalAirline(air.Airline):

    @staticmethod
    def convenient_offer(flight: modFl.AmalFlight, otherFlight: modFl.AmalFlight, model):
        actual_cost = model.delay_cost(flight, flight.currentDelay) + \
                      model.delay_cost(otherFlight, otherFlight.currentDelay)
        offer_cost = model.delay_cost(otherFlight, model.gdp_schedule[-1] - otherFlight.eta)

        return offer_cost < actual_cost

    def make_offer_list(self, model):
        if model.kind == "1":
            offer_list = []
            flight: modFl.AmalFlight
            otherFlight: modFl.AmalFlight
            for flight in self.flights:
                default_offer = AmalOffer(flight, flight.slot, flight, flight.slot)
                offer_list.append(default_offer)
                for otherFlight in self.flights:
                    if flight != otherFlight and self.convenient_offer(flight, otherFlight, model):
                        offer_list.append(AmalOffer(otherFlight, model.slot_indexes[-1], flight, flight.eta_slot))
            return offer_list

    def __init__(self, df_airline: pd.DataFrame, airline_index, model):

        super().__init__(df_airline, airline_index, model)

        self.offerList = self.make_offer_list(model)

        print(self.name, self.offerList)

    def get_offers_for_flight(self, flight):

        offer_for_flight_list = []

        for offer in self.offerList:
            if offer.flightDown == flight:
                offer_for_flight_list.append(offer)
            if offer.flightUp == flight:
                offer_for_flight_list.append(offer)

        return offer_for_flight_list

    def get_offer_slot_range(self, flight: modFl.AmalFlight):

        airline_offer = self.get_offers_for_flight(flight)
        default_offer = AmalOffer(flight, flight.slot, flight, flight.slot)
        off_list = airline_offer + [default_offer]
        last_slot = 0
        for offer in off_list:
            if offer.flightDown == flight and offer.atMost > last_slot:
                last_slot = offer.atMost
        return range(flight.eta_slot, last_slot)


"""
    def from_csv(self, df_airline):
        amal_offers = []
        df = df_airline[df_airline["amal offer"].notna()]
        if df.shape[0] > 0:
            num_offers = int(max(df["amal offer"]))
            for off_num in range(1, num_offers + 1):
                d = df[df["amal offer"] == off_num]
                flight_down = d[d["amal offer kind"] == "D"]["flight"].values[0]
                at_most = d[d["amal offer kind"] == "D"]["time not after"].values[0]
                flight_up = d[d["amal offer kind"] == "U"]["flight"].values[0]
                at_least = d[d["amal offer kind"] == "D"]["time not after"].values[0]
                amal_offers.append(AmalOffer(self.get_flight_by_name(flight_down), at_most,
                                             self.get_flight_by_name(flight_up), at_least))

        return amal_offers

"""
