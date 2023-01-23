from ..interface.defs import Endpoint, Method
from ..request import Request, Response
from .generic import GenericResponse, GenericTransaction


class RestoreInit(GenericTransaction):
    '''
    Initialize restore
    '''
    def __init__(self):
        self.request = Request(Endpoint.RESTORE, Method.POST, {})

    def setResponse(self, response: Response):
        self.response = GenericResponse(response)
