import sys
import json
import numpy
from datetime import datetime, date
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

def main():
    tweet_file = open(sys.argv[1])
    counter = 0
    dictCord = dict()
    keyList = list()

    n_err, n_tot = 0, 0
    x_width, y_width = [], []
    for line in tweet_file:
        n_tot = n_tot + 1
        try:
            tweet = json.loads(line.replace("\\\\u003ca",""))
            if tweet["geo"] != None:
                lat = tweet["geo"]["coordinates"][0]
                lon = tweet["geo"]["coordinates"][1]
                t_date =  datetime.strptime(tweet["created_at"],'%a %b %d %H:%M:%S +0000 %Y')
                print "Lat:",lat,", lon:", lon, ", date:", t_date
                #cord = geo["coordinates"]
                #clipedLat = int(cord[0]*10)*.1
                #clipedLon = int(cord[1]*10)*.1
                #strLoc = str(clipedLat) + ", " + str(clipedLon)
                #if strLoc in dictCord.keys():
                #    dictCord[strLoc] = dictCord[strLoc] + 1
                #else:
                #    dictCord[strLoc] = 1
                #    keyList.append(strLoc)
            else:
                if tweet["place"]["bounding_box"] != None:
                    box = tweet["place"]["bounding_box"]["coordinates"]
                    x1 = box[0][0][0]
                    y1 = box[0][0][1]
                    x2 = box[0][2][0]
                    y2 = box[0][1][1]
                    if x2-x1 < 0.2 and y1-y2 < 0.2:
                        x_width.append(x2-x1)
                        y_width.append(y2-y1)
                        lat = x1 + (x2-x1)/2
                        lon = y1 + (y2-y1)/2
                        t_date =  datetime.strptime(tweet["created_at"],'%a %b %d %H:%M:%S +0000 %Y')
                        print "Lat:",lat,", lon:", lon, ", date:", t_date
        except:
            n_err = n_err + 1

    print n_err, "errors out of", n_tot, "tweets"
    x_arr = numpy.array(x_width)
    y_arr = numpy.array(y_width)
    print "x mean: ", numpy.mean(x_arr), "+/-", numpy.std(x_arr)
    print "y mean: ", numpy.mean(y_arr), "+/-", numpy.std(y_arr)
    n, bins, patches = plt.hist(x_arr, 50, facecolor='green')
    #plt.show()

if __name__ == '__main__':
    main()
