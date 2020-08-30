import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import glob
files = glob.glob("/home/andrea/Scrivania/Tesi/implementazioni/results/*.csv")

plt.rcParams["figure.figsize"] = [20, 15]


save = True


def total_handle(df, save, title):
    plt.rcParams["figure.figsize"] = [10, 15]
    total= df[df["airline"]=="total"]
    initial = total["initial"]
    max_reduction = np.mean(1-total["max_reduction"]/initial)
    udpp = np.mean(1-total["udpp"]/initial)
    model = np.mean(1-total["model"]/initial)
    offers = np.mean(total["offers"])
    plt.bar([0,0.15,0.3],[max_reduction,udpp,model],width=0.1,label=[max_reduction,udpp,model,offers])
    plt.legend()
    plt.title("total reduction "+title)
    if save:
        plt.savefig("plots/total reduction "+title+".png")
        plt.show()
    else:
        plt.show()
len(df["run"].unique())

def airlines_plot(df, save, title):
    plt.rcParams["figure.figsize"] = [20, 15]
    runs= len(df["run"].unique())
    airlines=df[df["airline"]!="total"]
    num_flights = np.sort(airlines["num_flights"].unique())
    offers = []
    flights = []
    for i in num_flights:
        df_temp=airlines[airlines["num_flights"]==i]
        offers.append(sum(df_temp["offers"]))
        flights.append(df_temp.shape[0])
    offers=np.array(offers)/sum(offers)
    flights=np.array(flights)/runs
    #plt.bar(range(len(offers)),flights,label=flights)

    plt.bar(range(len(offers)),offers,label=offers)
    plt.yticks(np.arange(0,0.31,0.05))
    plt.xticks(range(len(offers)),num_flights)
    plt.legend()
    plt.title("airlines "+title)
    if save:
        plt.savefig("plots/airlines "+title+".png")
        plt.show()
    else:
        plt.show()

def airlines_riduction(df, save, title):
    plt.rcParams["figure.figsize"] = [20, 15]
    airlines=df[df["airline"]!="total"]
    num_flights = np.sort(airlines["num_flights"].unique())
    max_reduction = []
    udpp = []
    model = []
    for i in num_flights:
        df_temp=airlines[airlines["num_flights"]==i]
        initial = df_temp["initial"]
        max_reduction.append(np.mean(1-df_temp["max_reduction"]/initial))
        udpp.append(np.mean(1-df_temp["udpp"]/initial))
        model.append(np.mean(1-df_temp["model"]/initial))
    # plt.plot(num_flights,max_reduction, label="max", linewidth = 2.5)

    plt.bar(num_flights,model,label=model)
    plt.bar(num_flights,udpp, label=udpp)
    plt.legend()
    plt.title("airlines "+title)
    if save:
        plt.savefig("plots/airlines_reduction_"+title+".png")
        plt.show()
    else:
        plt.show()




for file in files:
    df= pd.read_csv(file)
    total_handle(df,save,file[52:-4])
for file in files:
    df= pd.read_csv(file)
    airlines_plot(df,save,file[52:-4])
for file in files:
    df= pd.read_csv(file)
    airlines_riduction(df,save,file[52:-4])


df
df = pd.read_csv("70_0.csv")
airlines = df[df["airline"]!="total"]
dist = []
for i in np.sort(airlines["num_flights"].unique()):
    dist.append(airlines[airlines["num_flights"]==i].shape[0])
dist= np.array(dist)/airlines["run"].unique().shape[0]
plt.bar(range(len(dist)),dist,label=dist)
plt.legend()
plt.xticks(range(len(dist)),np.sort(airlines["num_flights"].unique()))
plt.xlabel("NUMBER OF FLIGHTS PER AIRLINE")
plt.ylabel("NUMBER OF AIRLINES")
plt.title("Average distribution of flights among the airlines")
plt.savefig("airline_dist_70.png")





df = pd.read_csv("50_0.csv")
airlines=df[df["airline"]!="total"]
num_flights = np.sort(airlines["num_flights"].unique())
for i in num_flights[:1]:
    df_temp=airlines[airlines["num_flights"]==i]
    initial = df_temp["initial"]
    max_reduction = np.mean(1-df_temp["max_reduction"]/initial)
    udpp = np.mean(1-df_temp["udpp"]/initial)
    model = np.mean(1-df_temp["model"]/initial)
    print(max_reduction)
    plt.plot(max_reduction, label="max")
    plt.plot(udpp, label="udpp")
    plt.plot(model,label="model")
    #plt.xticks(range(len(offers)),num_flights)
    plt.legend()
    plt.title("airlines ")
    if save:
        plt.savefig("plots/airlines "+title+".png")
        plt.show()
    else:
        plt.show()
