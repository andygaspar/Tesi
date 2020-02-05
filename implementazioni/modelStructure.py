from airline import *

class modelStructure:

    def compute_delays(self):
        delays=np.zeros((self.num_flights,self.num_flights))
        for i,j in product(self.slots,self.slots):
            delays[i,j]=self.FPFS[j]-self.ETA[i]
        return delays

    def compute_ETA_index(self,ETA):
        ETA_index=[]
        for i in ETA:
            j=0
            while j<len(ETA) and self.FPFS[j]<i:
                j+=1
            ETA_index.append(j)
        return ETA_index

    def __init__(self,airlines,ETA,FPFS_scheduling,model_name="model",f=lambda x: x):

        self.e=sys.float_info.min

        self.num_flights=len(ETA)
        self.num_airlines=len(airlines)
        self.airlines=np.array(airlines)

        self.ETA=np.array(ETA)
        self.FPFS=np.array(FPFS_scheduling)
        self.ETA_index=self.compute_ETA_index(self.ETA)

        self.slots=np.array([i for i in range(len(self.FPFS))])
        self.delays=self.compute_delays()
        for a in self.airlines:
            a.set_preferencies(f)

        self.new_schedule=[]
        self.solutionX=None
        self.solutionC=None
        self.m= Model(model_name)

        self.offers = []

    def __str__(self):
        return str(self.airlines)

    def __repr__(self):
        return str(self.airlines)

    def score(self,airline,i,j):
        return self.delays[i,j]*airline.preferences[i]

    def which_airline(self,flight):
        for a in self.airlines:
            if flight in a.flights:
                return a
    def get_flights_name(self,i):
        return self.which_airline(i).flights_name[i]

    def print_schedule(self):
        print("{0:^10}".format("AIRLINE"),"{0:^10}".format("FLIGTH"),\
        "{0:^10}".format("ETA"),"{0:^10}".format("DELAY"),"{0:^10}".format("COSTS"))

        for i in self.slots:
            print("{0:^10}".format(str(self.which_airline(i))),\
            "{0:^10}".format(self.which_airline(i).flights_name[i]),\
            "{0:^10}".format(self.ETA[i]),\
            "{0:^10}".format(self.delays[i,i]),\
            "{0:^10}".format(self.which_airline(i).preferences[i]*self.delays[i,i]))

    def print_solution(self):
        print("{0:^10}".format("AIRLINE"),"{0:^10}".format("FLIGTH"),\
        "{0:^10}".format("ETA"),"{0:^10}".format("DELAY"),"{0:^10}".format("COSTS"))

        for sol in self.new_schedule:
            print("{0:^10}".format(str(self.which_airline(sol[0]))),\
            "{0:^10}".format(self.which_airline(sol[0]).flights_name[sol[0]]),\
            "{0:^10}".format(self.ETA[sol[0]]),\
            "{0:^10}".format(self.delays[sol[0],sol[1]]),\
            "{0:^10}".format(self.which_airline(sol[0]).preferences[sol[0]]*self.delays[sol[0],sol[1]]))






    def find_match(self, i):
        for j in self.slots[self.slots != i]:
            if self.solutionX[i, j].x == 1:
                return j

    #
    # def print_costs:
    #     for airline in self.airlines:
    #         costs=0
    #         for
    #

    def is_in_list(self,List,elem):
        for el in List:
            if np.array_equiv(el,elem):
                return True
        return False

    def print_offers(self):
        tuple_found=[]
        for off in self.offers:
            if not self.is_in_list(tuple_found,off[1]):
                airA=off[0]
                airB=self.which_airline(self.find_match(off[1][0]))
                print("{0:^5}".format(str(airA)),"{0:^15}".format(str(airB)))
                new_tuple=[]
                for flight in off[1]:
                    match=self.find_match(flight)
                    print("{0:^5}".format(airA.flights_name[flight])," -> ","{0:^5}".format(airB.flights_name[match]),\
                        " -> ","{0:^5}".format(airA.flights_name[self.find_match(match)]))
                    new_tuple.append(self.find_match(flight))
                tuple_found.append(off[1])
                tuple_found.append(np.sort(new_tuple))
