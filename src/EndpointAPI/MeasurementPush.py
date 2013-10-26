'''
Created on Oct 26, 2013

@author: diegob
'''

from protorpc import messages, message_types


class MeasurementPush(messages.Message):
    '''
    classdocs
    '''
    timestamp = message_types.DateTimeField(1, required=True)
    lat = messages.FloatField(2, required=True)
    lon = messages.FloatField(3, required=True)
    sensorValue = messages.FloatField(4, required=True)