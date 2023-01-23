from enum import Enum

from ..interface.defs import Endpoint, Method, PureLogLevel
from ..request import Request, Response
from .generic import GenericResponse, GenericTransaction


class PhoneModeLock(GenericTransaction):
    '''
    disable phoneLockCodeEnabled
    for some reason unlocks developer mode too (without it we can have 403 codes on calls to it)
    INFO: sets phone_mode_lock state in current harness session
    '''
    def __init__(self, enable: bool):
        self.enabled = enable
        self.request = Request(Endpoint.DEVELOPERMODE, Method.PUT, {"phoneLockCodeEnabled": enable})

    def setResponse(self, response: Response):
        self.response = GenericResponse(response)

    def onRun(self, harness):
        harness.set_phone_mode_lock_state(self.enabled)

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

class SetEQ(GenericTransaction):
    '''
    Overwrites EQ files to be able to change the EQ without entering the bootloader.
    Filename must match names on the phone, data is just a string with content of the file.
    '''
    def __init__(self, file_name: str, file_data: str):
        self.request = Request(Endpoint.DEVELOPERMODE, Method.PUT,  {"EQ": "test", "fileName": file_name, "fileData":file_data})

    def setResponse(self, response: Response) -> GenericResponse:
        self.response = GenericResponse(response)
