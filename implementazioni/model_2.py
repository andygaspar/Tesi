from model import *

class model_2(model):

    def __init__(self,airlines,ETA,FPFS_scheduling,f=lambda x: x):
        super().__init__(airlines,ETA,FPFS_scheduling,f=lambda x: x)
        self.airlines_pairs=pairs(self.airlines)
        self.c = np.array([[self.m.add_var(var_type=BINARY) for i in airline.flight_pairs] for airline in self.airlines])
        self.x = np.array([[self.m.add_var(var_type=BINARY) for i in self.slots] for j in self.slots])

    def run(self):

        x = np.array([[self.m.add_var(var_type=BINARY) for i in self.slots] for j in self.slots])

        c = np.array([[self.m.add_var(var_type=BINARY) for i in airline.flight_pairs] for airline in self.airlines])
        print(c)

        for i in range(len(self.slots)):
            self.m += xsum(x[i,j] for j in self.slots) == 1

        for j in range(len(self.slots)):
            self.m += xsum(x[i,j] for i in self.slots) <= 1


        for air_pair in self.airlines_pairs:
            airlineA=air_pair[0].flight_pairs
            airlineB=air_pair[1].flight_pairs
            for pairA in airlineA:
                for pairB in airlineB:
                    self.m += xsum(x[i,j] for i in pairA for j in pairB) + xsum(x[j,i] for i in pairA for j in pairB)\
                     <= (c[ind(problem.airlines,air_pair[0])][ind(airlineA,pairA)] \
                     + c[np.where(problem.airlines == air_pair[1])][np.where(airlineB == pairB)])*2

                    self.m += xsum(x[i,j] * self.score(air_pair[0],i,j) for i in pairA for j in pairB) <= \
                    xsum(x[i,j] * self.score(v,i,i) for i in pairA for j in pairB)-self.e


        self.m.objective= minimize(xsum(x[i,j]*self.score(a,i,j) for a in self.airlines for i in a.flights for j in self.slots))

        self.m.optimize()
        self.solution=x

        for j in self.slots:
            for i in self.slots:
                if x[i,j].x!=0:
                    self.new_schedule.append((i,j))


def ind(array,elem):
    print("ciccio",np.where(array == elem))
    return np.where(array == elem)[0]


BA=airline("BA",[1,4,5],[4,9,12])
YA=airline("YA",[0,2,3,6],[1,14,1,15])

ETA=np.array(range(7))
FPFS=ETA*2

problem=model_2([BA,YA],ETA,FPFS)
problem.run()


c = np.array([[i for i in airline.flight_pairs] for airline in problem.airlines])
for i in c:
    print(i)

for air_pair in problem.airlines_pairs:
    airlineA=air_pair[0].flight_pairs
    airlineB=air_pair[1].flight_pairs
    for pairA in airlineA:
        for pairB in airlineB:
            print(ind(problem.airlines,air_pair[0]))
            print(pairA)
            print(airlineA)
            print(ind(airlineA,pairA))
            print(c[ind(problem.airlines,air_pair[0])][ind(airlineA,pairA)] )
            # + c[np.where(problem.airlines == air_pair[1])][np.where(airlineB == pairB)])*2


a=[[1,2],[3,4],[5,6]]

np.where()

problem.run()

problem.print_schedule()
problem.print_solution()
problem.print_offers()
