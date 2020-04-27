import pandas as pd
from Programma.Amal import amalFlight as modFl
from Programma.ModelStructure.Airline import airline as air
from Programma.Amal import offerMaker as oM


class AmalAirline(air.Airline):

    @staticmethod
    def convenient_offer(flight: modFl.AmalFlight, otherFlight: modFl.AmalFlight, model):
        actual_cost = model.delay_cost(flight, flight.currentDelay) + \
                      model.delay_cost(otherFlight, otherFlight.currentDelay)
        offer_cost = model.delay_cost(otherFlight, model.gdp_schedule[-1] - otherFlight.eta)

        return offer_cost < actual_cost

    def __init__(self, df_airline: pd.DataFrame, airline_index, model):

        flight: modFl.AmalFlight

        super().__init__(df_airline, airline_index, model)

        self.offerList = oM.make_offer_list(model, self)

        for flight in self.flights:
            flight.set_flight_offer_properties(self.get_offers_for_flight(flight))

    def get_offers_for_flight(self, flight):

        offer_for_flight_list = []

        for offer in self.offerList:
            if offer.flightDown == flight:
                offer_for_flight_list.append(offer.atMost)
            elif offer.flightUp == flight:
                offer_for_flight_list.append(offer.atLeast)

        return offer_for_flight_list



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
