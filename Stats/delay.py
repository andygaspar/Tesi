import numpy as np
import pandas as pd
import matplotlib.pyplot as plt




plt.rcParams["figure.figsize"]=(15,10)
plt.rcParams["font.size"]=20



#en route....

years=np.array([i for i in range(2011,2020)])

enroute_delay=np.array([11238639,6004683,5005985,5806501,7167424,8665163,9282426,18957977,16310891])

flights=np.array([9868661,9633979,9529503,9699825,9854487,10117411,10514510,10905314,10208076])

plt.plot(years,enroute_delay)
plt.xticks(years)
plt.annotate('Datasource: Eurocontrol', (0,0), (300,-30), fontsize=20,
             xycoords='axes fraction', textcoords='offset points', va='top')
plt.title("EN-ROUTE DELAY")
plt.savefig("enroute_delay.png",bbox_inches="tight")




plt.plot(years,flights)
plt.xticks(years)
plt.annotate('Datasource: Eurocontrol', (0,0), (300,-30), fontsize=20,
             xycoords='axes fraction', textcoords='offset points', va='top')
plt.title("FLIGHTS EN-ROUTE DELAYED")
plt.savefig("enroute_fligths.png",bbox_inches="tight")




# airport

a_flights=np.array([118122,100259,102033,101241])
a_years=np.array([i for i in range(2016,2020)])


plt.plot(a_years,a_flights)
plt.xticks(a_years)
plt.annotate('Datasource: Eurocontrol', (0,0), (300,-30), fontsize=20,
             xycoords='axes fraction', textcoords='offset points', va='top')
plt.title("AIRPORT DELAY")
plt.savefig("airport_delay.png",bbox_inches="tight")

a_delay=np.array([161582,168357,169899,156698])



plt.plot(a_years,a_delay)
plt.xticks(a_years)
plt.annotate('Datasource: Eurocontrol', (0,0), (300,-30), fontsize=20,
             xycoords='axes fraction', textcoords='offset points', va='top')
plt.title("FLIGHTS AIRPORT DELAYED")
plt.savefig("airport_flights.png",bbox_inches="tight")
