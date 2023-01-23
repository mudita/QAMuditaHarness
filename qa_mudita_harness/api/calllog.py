from ..interface.defs import Endpoint, Method
from ..request import Request, Response
from .generic import GenericResponse, GenericTransaction


class CallLogsCountResponse(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.count = self.response.body["count"]


class CallLogsResponse(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entries = self.response.body["entries"]
        self.totalCount = self.response.body["totalCount"]


class CallLogByIdResponse(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entry = self.response.body


class GetCallLogsCount(GenericTransaction):
    """
    Get the count of call logs
    """

    def __init__(self):
        self.request = Request(Endpoint.CONTACTS, Method.GET, {"count": True})

    def setResponse(self, response: Response):
        self.response = CallLogsCountResponse(response)


class GetCallLogsWithOffsetAndLimit(GenericTransaction):
    """
    Retrieve call logs with offset and limit
    """

    def __init__(self, offset: int, limit: int):
        self.request = Request(Endpoint.CALLLOG, Method.GET, {"offset": offset, "limit": limit})

    def setResponse(self, response: Response):
        self.response = CallLogsResponse(response)


class GetCallLogById(GenericTransaction):
    """
    Retrieve call log by id
    """

    def __init__(self, id: int):
        self.request = Request(Endpoint.CALLLOG, Method.GET, {"id": id})

    def setResponse(self, response: Response):
        self.response = CallLogByIdResponse(response)


class DeleteCallLogById(GenericTransaction):
    """
    Delete call log with specified id
    """

    def __init__(self, id: int):
        self.request = Request(Endpoint.CALLLOG, Method.DEL, {"id": id})

    def setResponse(self, response: Response):
        self.response = GenericResponse(response)
