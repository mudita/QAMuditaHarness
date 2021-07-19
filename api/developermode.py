from harness.request import Request, Response
from harness.interface.defs import Endpoint, Method, PureLogLevel
from enum import Enum
from .generic import GenericResponse, GenericTransaction


class PhoneModeLock(GenericTransaction):
    '''
    disable phoneLockCodeEnabled
    for some reason unlocks developer mode too (without it we can have 403 codes on calls to it)
    '''
    def __init__(self, enable: bool):
        self.request = Request(Endpoint.DEVELOPERMODE, Method.PUT, {"phoneLockCodeEnabled": enable})

    def setResponse(self, response: Response):
        self.response = GenericResponse(response)


class Reboot(Enum):
    UPDATE = True


class PhoneReboot(GenericTransaction):
    '''
    Requests for Phone reboot, right now with "update" reason
    '''
    def __init__(self, type: Reboot):
        self.request = Request(Endpoint.DEVELOPERMODE, Method.POST, {"update": True, "reboot": type.value})

    def setResponse(self, response: Response):
        self.response = GenericResponse(response)


class SetLog(GenericTransaction):
    '''
    Sets log level for selected service, can be used to limit spamming logs on phone
    '''
    def __init__(self, service: str, level: PureLogLevel):
        self.request = Request(Endpoint.DEVELOPERMODE, Method.PUT, {"log": True, "service": service, "level": level.value})

    def setResponse(self, response: Response) -> GenericResponse:
        self.response = GenericResponse(response)


class GetLog(GenericTransaction):
    '''
    Get Log level for selected service
    '''
    def __init__(self, service: str, level: PureLogLevel):
        self.request = Request(Endpoint.DEVELOPERMODE, Method.GET, {"log": True, "service": service})

    def setResponse(self, response: Response) -> GenericResponse:
        self.response = GenericResponse(response)
