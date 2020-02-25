import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os



schedule=pd.read_csv("data/gdp_schedule.csv")
request=pd.read_csv("data/request.csv")
schedule
request
df=schedule.copy(deep=True)




#initial gdp_schedule
schedule=[]
for i in range(df.shape[0]):
    schedule.append(int(df.iloc[i]["eta"][0:2])*60+int(df.iloc[i]["eta"][3:5]))
df["initial gdp_schedule"]=schedule


#udpp gdp_schedule
df["udpp"]=df["initial gdp_schedule"]+df["delay udpp"]


#compute priority
df["priority"]=np.zeros(df.shape[0])
df["priority"]=request["request"]-request["base delay"]
df["priority"]+=abs(min(df["priority"]))





df_final=df[["flight","initial gdp_schedule","udpp","priority"]].copy(deep=True)
df_final.sort_values("udpp",inplace=True)


airlines=[]
for i in range(df.shape[0]):
    airlines.append(str.split(df_final.iloc[i]["flight"])[0])



df_final["airline"]=airlines
df_final

df_final.to_csv("ruiz.csv")
