'''
Created on Oct 26, 2013

@author: diegob
'''
import numpy as np

def predictSingleValue(m, newPoint):
    p = m[0]*newPoint.lat + m[1]*newPoint.lon + m[2]
    return p

def calculateLinearModel(points):
    xVector = [x.location.lat for x in points]
    yVector = [y.location.lon for y in points]
    zVector = [z.sensorReading for z in points]
    data = np.array([xVector, yVector, np.ones(len(xVector))]).transpose()
    m = np.linalg.lstsq(data, zVector)[0]
    return m