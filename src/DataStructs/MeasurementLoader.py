'''
Created on Oct 26, 2013

@author: diegob
'''

import DataStructs.Measurement
import datetime
from google.appengine.ext.ndb import GeoPt
from google.appengine.tools import bulkloader


class MeasurementLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'Measurement',
                                   [('time', lambda x: datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S")),
                                    ('userID', str),
                                    ('location',
                                     lambda x: GeoPt(float(x.split(':')[0]), float(x.split(':')[1]))),
                                    ('sensorReading', float)
                                   ])

loaders = [MeasurementLoader]
        