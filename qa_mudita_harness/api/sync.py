from ..interface.defs import Endpoint, Method
from ..request import Request, Response
from .generic import GenericResponse, GenericTransaction


class RequestSyncPackagePreparationResponse(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.taskId = self.response.body["id"]


class SyncPackagePreparationStateResponse(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = self.response.body["state"]
        if self.state == "error":
            self.reason = self.response.body["reason"]


class RequestSyncPackagePreparation(GenericTransaction):
    """
    Request sync package preparation
    """

    def __init__(self):
        self.request = Request(
            Endpoint.BACKUP,
            Method.POST,
            {
                "category": "sync",
            },
        )

    def setResponse(self, response: Response):
        self.response = RequestSyncPackagePreparationResponse(response)


class GetSyncPackagePreparationState(GenericTransaction):
    """
    Check sync package preparation status
    """

    def __init__(self, id: str):
        self.request = Request(
            Endpoint.BACKUP, Method.GET, {"category": "sync", "id": id}
        )

    def setResponse(self, response: Response):
        self.response = SyncPackagePreparationStateResponse(response)
