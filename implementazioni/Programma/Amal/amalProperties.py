import numpy as np
import pandas as pd
from Programma.Amal.amalOffer import AmalOffer
from Programma.Airline import airline as air


class AmalProperties:

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

    def make_offer_list(self, kind, df_airline):

        if kind == "fromCsv":
            return self.from_csv(df_airline)

    def __init__(self, kind: str, df_airline: pd.DataFrame) -> object:

        self.offerList = self.makeOfferList(kind, df_airline)

    def get_offers_for_flight(self, flight):

        offer_for_flight_list = []

        for offer in self.offerList:
            if offer.flightDown == flight:
                offer_for_flight_list.append(offer.atMost)
            if offer.flightUp == flight:
                offer_for_flight_list.append(offer.atLeast)

        return offer_for_flight_list
