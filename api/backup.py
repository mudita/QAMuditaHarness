from ..harness import Harness
from ..request import Request, Response
from ..interface.defs import Endpoint, Method
from .. import log
from .generic import GenericResponse, GenericTransaction


class BackupInitResponse(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.taskId = self.response.body["id"]
        self.state = self.response.body["state"]

class BackupStateResponse(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.taskId = self.response.body["id"]
        self.state = self.response.body["state"]
        if self.state == "error":
            self.reason = self.response.body["reason"]

class BackupInit(GenericTransaction):
    '''
    Initialize backup
    '''
    def __init__(self):
        self.request = Request(Endpoint.BACKUP, Method.POST, {})

    def setResponse(self, response: Response):
        self.response = BackupInitResponse(response)

class BackupGetState(GenericTransaction):
    '''
    Retrieve backup progress state
    '''
    def __init__(self, id: str):
        self.request = Request(Endpoint.BACKUP, Method.GET, {"id": id})

    def setResponse(self, response: Response):
        self.response = BackupStateResponse(response)
