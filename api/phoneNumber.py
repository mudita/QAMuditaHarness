from ..request import Request, Response
from ..interface.defs import Endpoint, Method
from .generic import GenericResponse, GenericTransaction


class GetNumberByNumberID(GenericTransaction):
    """
    Retrieve number form numberId
    """

    def __init__(self, numberID: int):
        self.request = Request(Endpoint.PHONENUMBER, Method.GET, {"numberID": numberID})

    def setResponse(self, response: Response):
        self.response = PhoneNumber(response)


class PhoneNumber(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.number = self.response.body["number"]
        self.numberID = self.response.body["numberID"]
