import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


schedule=pd.read_csv("data/schedule.csv")
request=pd.read_csv("data/request.csv")

df=schedule.copy(deep=True)

df["request"]=np.zeros(df.shape[0])

for flight in np.unique(df["flight"]):

    df["request"]=np.where((df["flight"]==flight),request[request["flight"]==flight]["request"].values[0],df["request"])


schedule=[]
for i in range(df.shape[0]):
    schedule.append(int(df.iloc[i]["eta"][0:2])*60+int(df.iloc[i]["eta"][3:5]))


df["initial schedule"]=schedule

df["udpp"]=df["initial schedule"]+df["delay udpp"]


df_final=df[["flight","initial schedule","udpp","request"]].copy(deep=True)
df_final.sort_values("udpp",inplace=True)
df_final["request"]=df_final["request"].to_numpy().astype(int)


airlines=[]
for i in range(df.shape[0]):
    airlines.append(str.split(df_final.iloc[i]["flight"])[0])



df_final["airline"]=airlines


df_final.to_csv("ruiz")
