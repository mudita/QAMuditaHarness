from .interface.defs import Method, Status, Endpoint
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json


class TransmissionError(Exception):
    '''
    Generall transmission error to be used i.e. if data in communication is not available
    to be used i.e. in case when Response dataclass is not filled in
    '''
    pass


class TransactionError(Exception):
    '''
    Generall error during tranmission due to wrong Status
    should be risen if respose is of any other than OK or Accepted
    '''
    def __init__(self, status: Status, message="HTTP Transaction Error!"):
        self.status = status
        self.message = message


@dataclass_json
@dataclass
class Response:
    endpoint: Endpoint
    status: Status
    uuid: int
    body: dict = field(default_factory=dict)

    def validate(self):
        '''
        method used to throw on error - so that we would actually check
        if something was not done properly
        '''
        if (self.status is not Status.OK.value) and (self.status is not Status.Accepted.value):
            raise TransactionError(self.status)


@dataclass_json
@dataclass
class Request():
    endpoint: Endpoint
    method: Method
    body: dict = field(default_factory=dict)
    uuid: int = -1


class Transaction:
    def __init__(self, request: Request):
        self.request = request

    def accept(self, resp: dict) -> None:
        self.response = Response(**resp)
        self.response.validate()

    def set_elapsed(self, send, read):
        self.send_time = send
        self.read_time = read
