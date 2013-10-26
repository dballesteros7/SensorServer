'''
Created on Oct 26, 2013

@author: diegob
'''
from google.appengine.ext import db
from google.appengine.ext.db import DateTimeProperty, StringProperty, GeoPtProperty, FloatProperty

class Measurement(db.Model):
    '''
    classdocs
    '''
    
    time = DateTimeProperty()
    userID = StringProperty()
    location = GeoPtProperty()
    sensorReading = FloatProperty()
    
    @classmethod
    def queryMeasurements(cls, startTime, endTime):
        q= cls.all()
        q.filter("time >", startTime)
        q.filter("time <", endTime)
        return q
        