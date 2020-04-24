import numpy as np
from Programma.Amal.amalOffer import AmalOffer


class AmalProperties:

    def from_csv(self, df_airline):
        amal_offers = []
        df = df_airline[df_airline["amal offer"].notna()]
        if df.shape[0] > 0:
            num_offers = int(max(df["amal offer"]))
            for off_num in range(1, num_offers + 1):
                d = df[df["amal offer"] == off_num]
                flightDown = d[d["amal offer kind"] == "D"]["flight"].values[0]
                atMost = d[d["amal offer kind"] == "D"]["time not after"].values[0]
                flightUp = d[d["amal offer kind"] == "U"]["flight"].values[0]
                atLeast = d[d["amal offer kind"] == "D"]["time not after"].values[0]
                amal_offers.append(AmalOffer(self.get_flight_by_name(flightDown), atMost,
                                             self.get_flight_by_name(flightUp), atLeast))

        return amal_offers

    def makeOfferList(self, kind, df_airline):

        if kind == "fromCsv":
            return self.from_csv(df_airline)

    def __init__(self, kind: str, df_airline: object) -> object:

        self.offerList = self.makeOfferList(kind, df_airline)

    def getOffersForFlight(self, flight):

        offerForFlightList = []

        for offer in self.offerList:
            if offer.flightDown == flight:
                offerForFlightList.append(offer.atMost)
            if offer.flightUp == flight:
                offerForFlightList.append(offer.atLeast)

        return offerForFlightList
