import numpy as np

class Offer:
    def __init__(self, airline_a, airline_b, fl_a_in, fl_b_in, fl_a_final,fl_b_final):
        self.airl_a = airline_a
        self.airl_b = airline_b
        self.flight_a_init = fl_a_in
        self.flight_b_init = fl_b_in
        self.flight_a_final = fl_a_final
        self.flight_b_final = fl_b_final

    # def __str__(self):
    #     return str("{0:^5}".format(self.flight_a_init), " -> ", "{0:^5}".format(self.flight_a_final),
    #           " -> ", "{0:^5}".format(self.))