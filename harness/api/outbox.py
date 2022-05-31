from ..request import Request, Response
from ..interface.defs import Endpoint, Method
from .generic import GenericResponse, GenericTransaction
from enum import Enum


class NotificationType(Enum):
    INVALID = 0
    MESSAGE = 1
    THREAD = 2
    CONTACT = 3


class NotificationChange(Enum):
    INVALID = 0
    CREATED = 1
    UPDATED = 2
    DELETED = 3


class NotificationEntry:
    def __init__(self, uid: int, type: NotificationType, change: NotificationChange, record_id: int):
        self.uid = uid
        self.type = type
        self.change = change
        self.record_id = record_id


class NotificationsResponse(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entries = []
        for entry in self.response.body["entries"]:
            self.entries.append(NotificationEntry(entry["uid"], entry["type"], entry["change"], entry["record_id"]))


class GetNotifications(GenericTransaction):
    """
    Retrieve notifications
    """

    def __init__(self):
        self.request = Request(Endpoint.OUTBOX, Method.GET, {"category": "entries"})

    def setResponse(self, response: Response):
        self.response = NotificationsResponse(response)


class DeleteNotifications(GenericTransaction):
    """
    Delete notifications with specified uid
    """

    def __init__(self, entries: list):
        self.request = Request(Endpoint.OUTBOX, Method.DEL, {"entries": entries})

    def setResponse(self, response: Response):
        self.response = GenericResponse(response)
