from .interface.defs import Method, Status, Endpoint
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json


class TransmissionError(Exception):
    '''
    General transmission error to be used i.e. if data in communication is not available
    to be used i.e. in case when Response dataclass is not filled in
    '''
    pass


class TransactionError(Exception):
    '''
    General error during tranmission due to wrong Status
    should be risen if respose is of any other than OK or Accepted
    '''
    def __init__(self, status: Status, message="HTTP Transaction Error!"):
        self.status = status
        self.message = message


@dataclass_json
@dataclass
class Response:
    '''
    pseudo REST response from Phone,
    at minimum contains Status which represents andy of HTTP status codes
    '''
    endpoint: Endpoint
    status: Status
    uuid: int
    body: dict = field(default_factory=dict)

    def validate(self):
        '''
        method used to throw an error - so that we would actually check
        if something was not done properly, or there was HTTP error
        '''
        if ((self.status >= Status.BadRequest.value)):
            raise TransactionError(self.status)


@dataclass_json
@dataclass
class Request():
    '''
    pseudo REST request sent to phone
    at minimum has to have Endpoint, Method and UUID
    '''
    endpoint: Endpoint
    method: Method
    body: dict = field(default_factory=dict)
    uuid: int = -1


class Transaction:
    '''
    Class binding Request -> Response behavior
    and providing additionall data about that exchange,
    which for now is execution time
    '''
    def __init__(self, request: Request):
        self.request = request

    def accept(self, resp: dict) -> None:
        self.response = Response(**resp)
        self.response.validate()

    def set_elapsed(self, send, read):
        '''
        Sets execution time spend on:
            - sending
            - receiving
        enables evaluation on how long we spend doing some action
        '''
        self.send_time = send
        self.read_time = read
