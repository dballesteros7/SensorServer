'''
Created on Oct 26, 2013

@author: diegob
'''

from datetime import datetime
import logging
import os

from google.appengine.ext.ndb.model import GeoPt
import jinja2
import numpy
import webapp2

from DataStructs.Measurement import Measurement
from Predictors import LinearExtrapolation


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MapDisplay(webapp2.RequestHandler):
    '''
    classdocs
    '''        
    
    def get(self):
        args = self.request.arguments()
        startTime = datetime.utcfromtimestamp(0)
        endTime = datetime.utcnow()
        if('time_start' in args and self.request.get('time_start')):
            startTime = datetime.strptime(self.request.get('time_start'), '%m/%d/%Y')
        if('time_end' in args and self.request.get('time_end')):
            endTime = datetime.strptime(self.request.get('time_end'), '%m/%d/%Y')
        points = Measurement.queryMeasurements(startTime, endTime).fetch(None)
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({'points' : points,
                                             'maxTime' : endTime.strftime('%m/%d/%Y'),
                                             'minTime' : startTime.strftime('%m/%d/%Y')}))
            
    

class Predictor(webapp2.RequestHandler):
    '''
    classdocs
    '''   
    def RandomWalk(self, N=100, d=2):
        """
        Use numpy.cumsum and numpy.random.uniform to generate
        a 2D random walk of length N, each of which has a random DeltaX and
        DeltaY between -1/2 and 1/2.  You'll want to generate an array of 
        shape (N,d), using (for example), random.uniform(min, max, shape).
        Taken from: http://pages.physics.cornell.edu/~sethna/StatMech/ComputerExercises/PythonSoftware/RandomWalk.py
        """
        return numpy.cumsum(numpy.random.uniform(-0.01, 0.01, (N, d)), axis=0)
    
    def get(self):
        args = self.request.arguments()
        x = float(self.request.get('x'))
        y = float(self.request.get('y'))
        startTime = datetime.utcfromtimestamp(0)
        endTime = datetime.utcnow()
        if('time_start' in args and self.request.get('time_start')):
            startTime = datetime.strptime(self.request.get('time_start'), '%m/%d/%Y')
        if('time_end' in args and self.request.get('time_end')):
            endTime = datetime.strptime(self.request.get('time_end'), '%m/%d/%Y')
        points = Measurement.queryMeasurements(startTime, endTime).fetch(None)
        walk = self.RandomWalk(100000, 2)
        X, Y = numpy.transpose(walk)[0:2]
        X += numpy.expand_dims(x, axis=1)
        Y += numpy.expand_dims(y, axis=1)
        m = LinearExtrapolation.calculateLinearModel(points)
        for i in xrange(len(X)):
            p = LinearExtrapolation.predictSingleValue(m, GeoPt(Y[i], X[i]))
            points.append(Measurement(location = GeoPt(Y[i],X[i]), sensorReading = p))
            logging.info("%s,%s" % (X[i],Y[i]))
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({'points' : points,
                                             'maxTime' : endTime.strftime('%m/%d/%Y'),
                                             'minTime' : startTime.strftime('%m/%d/%Y')}))        
application = webapp2.WSGIApplication([
    ('/', MapDisplay),
    ('/query', Predictor)
], debug=True)
