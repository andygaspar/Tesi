
def make_offer_list(model, airline):

    from Programma.Amal import amalFlight as modFl
    from Programma.Amal.amalOffer import AmalOffer
    from Programma.Amal import amalAirline

    airline: amalAirline.AmalAirline
    if model.offerMakerFunType == "1":
        offer_list = []
        flight: modFl.AmalFlight
        otherFlight: modFl.AmalFlight
        for flight in airline.flights:
            default_offer = AmalOffer(flight, flight.slot, flight, flight.slot)
            offer_list.append(default_offer)
            for otherFlight in airline.flights:
                if flight != otherFlight and airline.convenient_offer(flight, otherFlight, model):
                    offer_list.append(AmalOffer(otherFlight, model.slot_indexes[-1], flight, flight.eta_slot))
        return offer_list
