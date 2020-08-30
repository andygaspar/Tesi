import numpy as np
import pandas as pd
import matplotlib.pyplot as plt




plt.rcParams["figure.figsize"]=(20,15)
plt.rcParams["font.size"]=20



#en route....

years=np.array([i for i in range(2013,2019)])

enroute_delay=np.array([5005985,5806501,7167424,8665163,9282426,18957977])

flights=np.array([7387558, 7430020, 7579885, 7857741, 8095934, 8323657])

plt.plot(years,flights,linewidth=3)
plt.xticks(years)
plt.yticks(np.arange(7.3,8.7,0.2)*1_000_000)
plt.annotate('Datasource: Eurocontrol', (0,0), (300,-30), fontsize=20,
             xycoords='axes fraction', textcoords='offset points', va='top')
plt.title("flights")
#plt.savefig("flights.png",bbox_inches="tight")


years=[str(i) for i in range(2013,2019)]
to_plot=[838920866, 876859730, 918249055, 972532157, 1043072331, 1105945753 ]
plt.plot(range(2013,2019),to_plot,linewidth=3)
plt.annotate('Datasource: Eurostat', (0,0), (300,-30), fontsize=20,
             xycoords='axes fraction', textcoords='offset points', va='top')
plt.yticks(np.arange(0.7,1.4,0.15)*1_000_000_000)
plt.xticks(range(2013,2019))
plt.savefig("passengers.png",bbox_inches='tight')



plt.plot(years,flights)
plt.xticks(years)
plt.annotate('Datasource: Eurocontrol', (0,0), (300,-30), fontsize=20,
             xycoords='axes fraction', textcoords='offset points', va='top')
plt.title("FLIGHTS EN-ROUTE DELAYED")
#plt.savefig("enroute_fligths.png",bbox_inches="tight")




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
