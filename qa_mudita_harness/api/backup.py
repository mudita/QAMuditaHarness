from ..interface.defs import Endpoint, Method
from ..request import Request, Response
from .generic import GenericResponse, GenericTransaction


class SyncInitResponse(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.taskId = self.response.body["id"]
        self.state = self.response.body["state"]

class SyncStateResponse(GenericResponse):
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
        self.request = Request(Endpoint.BACKUP, Method.POST, {
            "category": "backup"
        })

    def setResponse(self, response: Response):
        self.response = GenericResponse(response)

class SyncInit(GenericTransaction):
    '''
    Initialize backup
    '''
    def __init__(self):
        self.request = Request(Endpoint.BACKUP, Method.POST, {
            "category": "sync"
        })

    def setResponse(self, response: Response):
        self.response = SyncInitResponse(response)

class SyncGetState(GenericTransaction):
    '''
    Retrieve sync progress state
    '''
    def __init__(self, id: str):
        self.request = Request(Endpoint.BACKUP, Method.GET, {
            "category": "sync",
            "id": id
        })

    def setResponse(self, response: Response):
        self.response = SyncStateResponse(response)
