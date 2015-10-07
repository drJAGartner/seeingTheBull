import json
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt

if __name__ == "__main__":
    d0 = json.load(open("movieData.json"))

    mx, mx2, my, my2 = [], [], [], []
    for k, v in d0.iteritems():
        max_g = float(v["max"])
        for it in v["h_gross"]:
                mx.append(int(k))
                my.append(float(it)/max_g)

    net_average = np.array(filter(lambda x: x > 0.01, my)).mean()
    print net_average
    #net_deviation = np.array(my).std()
    #std_err = net_deviation/sqrt(len(my))
    #print net_average, net_deviation, std_err
    #m, b = np.polyfit(mx, my, 1)
    #print m, b

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plt.xlabel("Year")
    #plt.ylabel("Gross")
    plt.ylabel("Gross/Year's Max Gross")
    x = np.array([1979, 2016])
    ax1.plot(x, [net_average]*2, color='r')
    ax1.scatter(mx, my, s=25, c='g', marker='o', label='Horror Movie Grosses')
    #ax1.scatter(mx2, my2, s=10, c='r', marker='+', label='Yearly Max Gross')
    ax1.set_xlim(1979,2016)
    ax1.set_ylim(0,0.45)
    plt.legend(loc='upper left')
    plt.savefig("movie_gross_ratio.png")