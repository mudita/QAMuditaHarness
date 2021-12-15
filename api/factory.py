from ..request import Request, Response
from ..interface.defs import Endpoint, Method
from enum import Enum
from .generic import GenericResponse, GenericTransaction


class FactoryResetResponse(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.requestDone = self.response.body["factoryRequest"]

class FactoryReset(GenericTransaction):
    '''
    Requests to perform a factory reset
    '''
    def __init__(self):
        self.request = Request(Endpoint.FACTORY, Method.POST, {"factoryRequest": True})

    def setResponse(self, response: Response):
        self.response = FactoryResetResponse(response)
