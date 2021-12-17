from ..request import Request, Response
from ..interface.defs import Endpoint, Method
from .generic import GenericResponse, GenericTransaction


class PhoneLockTimeResponse(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.phoneLockTime = self.response.body["phoneLockTime"]


class GetPhoneLockStatus(GenericTransaction):
    '''
    Get the phone lock status
    '''
    def __init__(self):
        self.request = Request(Endpoint.USBSECURITY, Method.GET, {"category": "phoneLockStatus"})

    def setResponse(self, response: Response):
        self.response = GenericResponse(response)


class GetPhoneLockTime(GenericTransaction):
    '''
    Get the phone lock time
    '''
    def __init__(self):
        self.request = Request(Endpoint.USBSECURITY, Method.GET, {"category": "phoneLockTime"})

    def setResponse(self, response: Response):
        self.response = PhoneLockTimeResponse(response)


class SetPhoneLockOff(GenericTransaction):
    '''
    Set the phone lock off
    '''
    def __init__(self, passcode: list = None):
        if passcode is None:
            passcode = [3, 3, 3, 3]
        self.request = Request(Endpoint.USBSECURITY, Method.PUT, {"phoneLockCode": passcode})

    def setResponse(self, response: Response):
        self.response = GenericResponse(response)
