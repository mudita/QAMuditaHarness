from ..harness import Harness
from ..request import Request, Response
from ..interface.defs import Endpoint, Method
from .. import log
from .generic import GenericResponse, GenericTransaction


class RestoreResponse(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.taskId = self.response.body["id"]
        self.state = self.response.body["state"]
        if (self.state == "error"):
            self.reason = self.response.body["reason"]

class RestoreFileListResponse(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.files = self.response.body["files"]


class RestoreInit(GenericTransaction):
    '''
    Initialize restore
    '''
    def __init__(self, id: str):
        self.request = Request(Endpoint.RESTORE, Method.POST, {"restore": id})

    def setResponse(self, response: Response):
        self.response = RestoreResponse(response)

class RestoreGetBackupList(GenericTransaction):
    '''
    Process single call to put next chunk of data Pure -> PC
    '''
    def __init__(self):
        self.request = Request(Endpoint.RESTORE, Method.GET, {"request": "fileList"})

    def setResponse(self, response: Response):
        self.response = RestoreFileListResponse(response)

class RestoreGetState(GenericTransaction):
    '''
    Process single call to put next chunk of data Pure -> PC
    '''
    def __init__(self, id: str):
        self.request = Request(Endpoint.RESTORE, Method.GET, {"id": id})

    def setResponse(self, response: Response):
        self.response = RestoreResponse(response)
