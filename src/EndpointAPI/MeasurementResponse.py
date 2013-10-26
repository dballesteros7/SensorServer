'''
Created on Oct 26, 2013

@author: diegob
'''
from protorpc import messages


class MeasurementResponse(messages.Message):
    '''
    classdocs
    '''
    response = messages.StringField(1, required=True)
        