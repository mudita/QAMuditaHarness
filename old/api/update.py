from ..request import Request, Response
from ..interface.defs import Endpoint, Method
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

    def onRun(self, harness):
        harness.reboot_requested = True

class RebootToUsbMscMode(GenericTransaction):
    """
    Reboot device to USB MSC mode
    """

    def __init__(self):
        self.request = Request(Endpoint.UPDATE, Method.PUT, {"rebootMode": "usbMscMode"})

    def setResponse(self, response: Response):
        self.response = GenericResponse(response)
