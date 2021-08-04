from harness.request import Request, Response
from harness.interface.defs import Endpoint, Method, PureLogLevel
from enum import Enum
from .generic import GenericResponse, GenericTransaction


class Reboot(Enum):
    UPDATE = True

class PhoneReboot(GenericTransaction):
    '''
    Requests for Phone reboot, right now with "update" reason
    '''
    def __init__(self, type: Reboot):
        self.request = Request(Endpoint.UPDATE, Method.POST, {"update": True, "reboot": type.value})

    def setResponse(self, response: Response):
        self.response = GenericResponse(response)

