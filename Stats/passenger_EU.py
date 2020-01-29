import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv("passengers/avia_paoc_1_Data.csv")














df=df[df["TRA_MEAS"]=="Passengers carried"]


df=df.drop("UNIT",axis=1)
df=df.drop("TRA_MEAS",axis=1)
df=df.drop("SCHEDULE",axis=1)
df=df.drop("TRA_COV",axis=1)
df=df.drop("Flag and Footnotes",axis=1)


df=df[df["Value"]!=':']
vals=df["Value"].to_numpy()
new_vals=np.array([])
for i in vals:
    new_vals=np.append(new_vals,int(i.replace(',','')))

new_vals=new_vals.astype(int)
df["Value"]=new_vals


to_plot=df[df["GEO"]=="European Union - 27 countries (2007-2013)"]
to_plot

countries=np.unique(df["GEO"].to_numpy())
for i in countries:
    print(i)


plt.rcParams["figure.figsize"]=(15,10)
plt.rcParams["font.size"]=20

years=[str(i) for i in range(2007,2019)]

plt.plot(range(2007,2019),to_plot["Value"])
plt.annotate('Datasource: Eurostat', (0,0), (300,-30), fontsize=20,
             xycoords='axes fraction', textcoords='offset points', va='top')
plt.xticks(range(2007,2019))
plt.savefig("passengers.png",bbox_inches='tight')







#flights ************************


df=pd.read_csv("flights/avia_paoc_1_Data.csv")








df=df.drop("UNIT",axis=1)
df=df.drop("TRA_MEAS",axis=1)
df=df.drop("SCHEDULE",axis=1)
df=df.drop("TRA_COV",axis=1)
df=df.drop("Flag and Footnotes",axis=1)


df=df[df["Value"]!=':']
vals=df["Value"].to_numpy()
new_vals=np.array([])
for i in vals:
    new_vals=np.append(new_vals,int(i.replace(',','')))

new_vals=new_vals.astype(int)
df["Value"]=new_vals







to_plot=df[df["GEO"]=="European Union - 27 countries (2007-2013)"]
to_plot

countries=np.unique(df["GEO"].to_numpy())
for i in countries:
    print(i)


years=[str(i) for i in range(2007,2019)]

plt.plot(range(2007,2019),to_plot["Value"])
plt.annotate('Datasource: Eurostat', (0,0), (300,-30), fontsize=20,
             xycoords='axes fraction', textcoords='offset points', va='top')
plt.xticks(range(2007,2019))
plt.savefig("flights.png",bbox_inches='tight')















df_ok=pd.DataFrame()

for year in years:
    df_ok=df_ok.append(df[df["TIME"]==year])





#Plots ************************************
tot_passengers=np.array([])
for year in years:
    tot_passengers=np.append(tot_passengers,sum(df_ok[df_ok["TIME"]==year]["Value"]))



tot_passengers[-1]
plt.rcParams["figure.figsize"]=(15,10)
plt.rcParams["font.size"]=20
plt.plot([int(i) for i in years],tot_passengers)
plt.annotate('Datasource: Eurostat', (0,0), (300,-30), fontsize=20,
             xycoords='axes fraction', textcoords='offset points', va='top')
plt.savefig("passengers.png",bbox_inches='tight')


plt.bar(df_ok[df_ok["TIME"]=="2017"]["GEO"],df_ok[df_ok["TIME"]=="2017"]["Value"])
plt.xticks(rotation="vertical")






flights=np.array([])
for year in years:
    flights=np.append(flights,sum(df_ok[df_ok["TIME"]==year]["Value"]))



flights
plt.rcParams["figure.figsize"]=(15,10)
plt.rcParams["font.size"]=20
plt.plot([int(i) for i in years],flights)
plt.annotate('Datasource: Eurostat', (0,0), (300,-30), fontsize=20,
             xycoords='axes fraction', textcoords='offset points', va='top')
plt.savefig("flights.png",bbox_inches='tight')


plt.bar(df_ok[df_ok["TIME"]=="2017"]["GEO"],df_ok[df_ok["TIME"]=="2017"]["Value"])
plt.xticks(rotation="vertical")



sum(df_ok[df_ok["TIME"]=="2005"]["Value"])
sum(df_ok[df_ok["TIME"]=="2018"]["Value"])



sum(df_ok[df_ok["TIME"]=="2005"]["Value"])
sum(df_ok[df_ok["TIME"]=="2018"]["Value"])





#******* by month


df=pd.read_csv("flights/avia_paoc_1_Data.csv")
df[df["TIME"]=="2019M01"]
df=df.iloc[:13260]
df
df[df["TIME"]=="2005"]
df=df.iloc[6120:]
df=df[df["Value"]!=':']
vals=df["Value"].to_numpy()
new_vals=np.array([])
for i in vals:
    new_vals=np.append(new_vals,int(i.replace(',','')))

new_vals=new_vals.astype(int)
df["Value"]=new_vals
df
years=[str(i) for i in range(2005,2019)]

delete_countries=["Croatia","Bulgaria","Montenegro","Serbia","North Macedonia"]
for c in delete_countries:
    df=df[df["GEO"]!=c]
df=df.reset_index(drop=False)
df=df.reset_index(drop=False)
df=df.drop("level_0",axis=1)
df=df.drop("index",axis=1)
df=df.drop("UNIT",axis=1)
df=df.drop("TRA_MEAS",axis=1)
df=df.drop("SCHEDULE",axis=1)
df=df.drop("TRA_COV",axis=1)
df=df.drop("Flag and Footnotes",axis=1)


df_ok=df.copy(deep=True)


for year in years:
    df_ok=df_ok[df_ok["TIME"]!=year]


df_month=pd.DataFrame()
for i in range(df_ok.shape[0]):
    if df_ok["TIME"].iloc[i][-2]!="Q":
        df_month=df_month.append(df_ok.iloc[i])



time=df_month["TIME"]
df_month

YEAR=[]
MONTH=[]
for item in time:
    YEAR.append(item[0:4])
    YEAR[-1]=int(YEAR[-1])
    MONTH.append(int(item[5:]))
YEAR
MONTH
df_month["month"]=MONTH
df_month["year"]=YEAR
df_month=df_month.drop("TIME",axis=1)
df_month["year"].iloc[0]

mat=np.zeros((14,12))

for i in range(14):
    for j in range(12):
        to_sum=df_month[df_month["year"]==int(years[i])]
        to_sum=to_sum[to_sum["month"]==j+1]
        mat[i,j]=sum(to_sum["Value"])/sum(df[df["TIME"]==years[i]]["Value"])
mat


stats=np.mean(mat,axis=0)
plt.bar(range(1,13),stats*100)
plt.xticks(range(1,13))
plt.annotate('Datasource: Eurostat', (0,0), (300,-30), fontsize=20,
             xycoords='axes fraction', textcoords='offset points', va='top')
plt.savefig("month average.png",bbox_inches="tight")








# Analisi separata



df=pd.read_csv("flights/avia_paoc_1_Data.csv")



df=df.drop("UNIT",axis=1)
df=df.drop("TRA_MEAS",axis=1)
df=df.drop("SCHEDULE",axis=1)
df=df.drop("TRA_COV",axis=1)
df=df.drop("Flag and Footnotes",axis=1)


df=df[df["Value"]!=':']
vals=df["Value"].to_numpy()
new_vals=np.array([])
for i in vals:
    new_vals=np.append(new_vals,int(i.replace(',','')))

new_vals=new_vals.astype(int)
df["Value"]=new_vals



df=df[df["GEO"]!="European Union - 27 countries (2007-2013)"]

df=df[df["GEO"]!="European Union - 28 countries"]
df

fl=np.array([])
for i in np.unique(df["TIME"].to_numpy()):
    fl=np.append(fl,sum(df[df["TIME"]==i]["Value"]))


plt.plot(range(2005,2019),fl)
plt.xticks(range(2005,2019))
plt.annotate('Datasource: Eurostat', (0,0), (300,-30), fontsize=20,
             xycoords='axes fraction', textcoords='offset points', va='top')
plt.savefig("flights_sum.png",bbox_inches='tight')
