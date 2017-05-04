#!/bin/python
# peak_detect is a realtime peak detection algorithm based on smoothing
# z-scores, see Jean-Paul's answer on
# http://stackoverflow.com/questions/22583391/peak-signal-detection-in-realtime-timeseries-data 

import numpy as np

def peak_detect(y_data, lag=5, threshold=3.5, influence=0.0):
    signals = np.zeros_like(y_data)
    filtered_y = np.zeros_like(y_data)
    filtered_y[0:lag] = y_data[0:lag]
    avg_filter = np.zeros_like(y_data)
    std_filter = np.zeros_like(y_data)
    avg_filter[lag-1] = np.mean(y_data[0:lag])
    std_filter[lag-1] = np.std(y_data[0:lag])
    for i in range(lag, len(y_data)):
        if ((np.abs(y_data[i] - avg_filter[i-1])) > (threshold * std_filter[i-1])):
            if (y_data[i] > avg_filter[i-1]):
                signals[i] = 1
            else:
                signals[i] = -1
            filtered_y[i] = influence*y_data[i] + (1-influence)*filtered_y[i-1]
            avg_filter[i] = np.mean(filtered_y[(i-lag):i])
            std_filter[i] = np.std(filtered_y[(i-lag):i])
        else:
            signals[i] = 0
            filtered_y[i] = y_data[i] 
            avg_filter[i] = np.mean(filtered_y[(i-lag):i])
            std_filter[i] = np.std(filtered_y[(i-lag):i])
    return [signals, avg_filter, std_filter]


# testing
# change out the "data" entry with np.genfromtxt("data.csv") or something
if __name__ == "__main__":
    from pylab import *

    data = np.array([1,1,1.1,1,0.9,1,1,1.1,1,0.9,1,1.1,1,1,0.9,1,1,1.1,1,1,1,
                     1,1.1,0.9,1,1.1,1,1,0.9,1,1.1,1,1,1.1,1,0.8,0.9,1,1.2,0.9,
                     1,1,1.1,1.2,1,1.5,1,3,2,5,3,2,1,1,1,0.9,1,1,3,2.6,4,3,
                     3.2,2,1,1,0.8,4,4,2,2.5,1,1,1])
    #result = peak_detect(data)
    result = peak_detect(data, lag=30, threshold=5, influence=0)
    x = [i for i in range(0, len(data))]
    f = figure()
    plot(x, data, color='k', marker="", lw=2)
    plot(x, result[0], color='r', marker="", lw=2)
    plot(x, result[1], color='c', marker="", lw=2)
    plot(x, result[1] + result[2], color="g", marker="", lw=2)
    plot(x, result[1] - result[2], color="g", marker="", lw=2)
    show()

    
