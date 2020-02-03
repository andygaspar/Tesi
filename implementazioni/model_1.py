from model import *



class model_1(model):

    def __init__(self,airlines,ETA,FPFS_scheduling,f=lambda x: x):
        super().__init__(airlines,ETA,FPFS_scheduling,f=lambda x: x)


    def run(self):

        x = np.array([[self.m.add_var(var_type=BINARY) for i in self.slots] for j in self.slots])

        for i in range(len(self.slots)):
            self.m += xsum(x[i,j] for j in self.slots) == 1

        for j in range(len(self.slots)):
            self.m += xsum(x[i,j] for i in self.slots) <= 1

        for i,j in product(self.slots,self.slots):
            if j<self.ETA_index[i]:
                self.m+= x[i,j]==0

        for i,j in product(self.slots,self.slots):
            self.m += x[i,j]==x[j,i]

        for v in self.airlines:
            for w in self.airlines:
                if v.name!=w.name:
                    self.m += xsum(x[i,j] * self.score(v,i,j) for i in v.flights for j in w.flights) <= \
                    xsum(x[i,j] * self.score(v,i,i) for i in v.flights for j in w.flights)-self.e

        self.m.objective= minimize(xsum(x[i,j]*self.score(a,i,j) for a in self.airlines for i in a.flights for j in self.slots))

        self.m.optimize()
        self.solution=x

        for j in self.slots:
            for i in self.slots:
                if x[i,j].x!=0:
                    self.new_schedule.append((i,j))
