'''
Created on Oct 26, 2013

@author: diegob
'''

import endpoints
from google.appengine.ext import ndb
from protorpc import remote

from DataStructs.Measurement import Measurement
from EndpointAPI.MeasurementResponse import MeasurementResponse
from EndpointAPI.MeasurementPush import MeasurementPush


@endpoints.api(name = 'measuresApi', version = 'v1',
               description = 'Test API for measurement storage.')
class MeasurementApi(remote.Service):
    '''
    classdocs
    '''

    @endpoints.method(MeasurementPush, MeasurementResponse, path='submit',
                      http_method='POST')
    def submitMeasurement(self, request):
        user = getCurrentUser()
        measurement = Measurement(time = request.timestamp,
                                  userID = user,
                                  location = ndb.GeoPt(request.lat, request.lon),
                                  sensorReading = request.sensorValue)
        measurement.put()
        return MeasurementResponse(response = "Success")
    
def getCurrentUser():
    current_user = endpoints.get_current_user()
    if current_user is None:
        return "anonymous"
    return current_user.user_id()
        
        
application = endpoints.api_server([MeasurementApi])