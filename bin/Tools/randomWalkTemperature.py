'''
Created on Oct 26, 2013

@author: diegob
'''

from datetime import datetime
import httplib
import json
import sys
import time

import numpy


def RandomWalk(N=100, d=2):
    """
    Use numpy.cumsum and numpy.random.uniform to generate
    a 2D random walk of length N, each of which has a random DeltaX and
    DeltaY between -1/2 and 1/2.  You'll want to generate an array of 
    shape (N,d), using (for example), random.uniform(min, max, shape).
    Taken from: http://pages.physics.cornell.edu/~sethna/StatMech/ComputerExercises/PythonSoftware/RandomWalk.py
    """
    return numpy.cumsum(numpy.random.uniform(-0.01, 0.01, (N, d)), axis=0)

def main():
    walk = RandomWalk(1000, 2)
    X, Y = numpy.transpose(walk)[0:2]
    X += numpy.expand_dims(-74, axis=1)
    Y += numpy.expand_dims(7.4, axis=1)
    fileHandleR = open('/home/diegob/dataPasto.csv' ,'r')
    fileHandle = open('randomWalk.csv', 'w')
    fileHandleR.readline()
    line = fileHandleR.readline()
    while(line):
        tokens = line.split(',')
        print tokens
        if(tokens[5] != "NA"):
            fileHandle.write("%s,%s,%s:%s,%s\n" % (datetime.strptime(tokens[0], "%Y%m").strftime("%Y-%m-%dT%H:%M:%S"), "super",
                             1.4170, -77.2670, float(tokens[5])))
        line = fileHandleR.readline()
#    for i in xrange(len(X)):
#         params = json.dumps({'timestamp': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.00"), 'lon': X[i], 'lat': Y[i],
#                              'sensorValue' : numpy.random.normal(16, 3)})
#         headers = {"Content-type": "application/json"}
#         conn = httplib.HTTPConnection("localhost", 8080)
#         conn.request("POST", "/_ah/api/measuresApi/v1/submit", params, headers)
#         response = conn.getresponse()
#         conn.close()
        
    fileHandle.close()
        
if __name__ == '__main__':
    sys.exit(main())
