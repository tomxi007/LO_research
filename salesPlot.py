import csv, math
from numpy import *
from matplotlib.pyplot import *



class Interval:
    """Time Interval to Seconds"""
    hr = 3600;
    threeHr = 3*3600;
    sixHr = 6*3600;
    halfDay = 12*3600;
    day = 24*3600;
    halfWeek = 3.5*86400;
    week = 7*86400;
    biWeek = 14*86400;
    month = (365/12)*86400;

def csvread(filename):
    return array(list(csv.reader(open(filename,"rb"),delimiter=','))).astype('float')

def salesPlot(csvFile, hopSize, windowLength):
    "csvFile is strings; hop, winLen"    
    sales = csvread(csvFile)
    startTime = sales[0,0]
    endTime = sales[-1,0]
    hopPerWindow = windowLength / hopSize
    outLen = int(math.floor((endTime-startTime) / hopSize)+1)
    output = zeros((outLen,5))
    output[:,0] = r_[startTime:endTime:hopSize]  
    sIdx = 0; 
    
    for oIdx in range(outLen):
        cutoffTime = output[oIdx,0]
        orderTime = sales[sIdx,0]
        while (orderTime < cutoffTime):
            sIdx += 1
            orderTime = sales[sIdx,0]
                
        output[oIdx,2] = sIdx
        if oIdx+hopPerWindow-1 < outLen:
            output[oIdx+hopPerWindow-1,1] = sIdx
        
        start = output[oIdx,1]
        output[oIdx,3]= (output[oIdx,0]-startTime)/Interval.day  #X axis data (days)

        if output[oIdx,2] == 0:
            output[oIdx,4] = 0
            continue
        elif output[oIdx,1] == 0:
            start = 0
        else:
            start = output[oIdx,1]
        output[oIdx,4] = sum(sales[start:output[oIdx,2],1])/hopPerWindow
    
        
    figure()
    plot(output[:,3],output[:,4])
    # xlabel('days since start date')
    # ylabel('Expected sale in one %s, averaging over one %s'.format(hopSize, windowLength))


