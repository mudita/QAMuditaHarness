from ..request import Request, Response
from ..interface.defs import Endpoint, Method, PureLogLevel
from enum import Enum
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


class RemoveFile(GenericTransaction):
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.request = Request(Endpoint.DEVELOPERMODE, Method.PUT, {"fs": True, "removeFile": filename})

    def setResponse(self, response: Response) -> GenericResponse:
        self.response = GenericResponse(response)

class RenameFile(GenericTransaction):
    def __init__(self, filename: str, destfilename: str) -> None:
        self.filename = filename
        self.destfilename = destfilename
        self.request = Request(Endpoint.DEVELOPERMODE, Method.PUT, {"fs": True, "renameFile": filename, "destfilename": destfilename})

    def setResponse(self, response: Response) -> GenericResponse:
        self.response = GenericResponse(response)

class ListFiles(GenericTransaction):
    """
    Returns list of the files available in a directory
    """
    def __init__(self, directory: str) -> None:
        self.directory = directory
        self.request = Request(Endpoint.DEVELOPERMODE, Method.GET, {"fs": True, "listDir": directory})

    def setResponse(self, response: Response) -> GenericResponse:
        self.response = GenericResponse(response)
    
    def getResponse(self) -> dict:
        return self.response.response.body[self.directory]
