from ..harness import Harness
from ..request import Request, Response, TransactionError
from ..interface.defs import Endpoint, Method
from .. import log
from .generic import GenericResponse, GenericTransaction

'''
NewContactEntry = {
    "address": "",
    "altName": "",
    "email":   "",
    "blocked": True/False,
    "favourite": True/False,
    "ice":     True/False,
    "numbers": [
        ""
    ],
    "speedDial": "",
    "priName":   "",
    "note":      ""
}
'''

class ContactsCount(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.count = self.response.body["count"]

class Contacts(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entries = self.response.body["entries"]
        self.totalCount = self.response.body["totalCount"]

class ContactByIdEntry(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entry = self.response.body

class AddedContactId(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = self.response.body["id"]

class DeletedContact(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class GetContactsCount(GenericTransaction):
    '''
    Get the count of contacts
    '''
    def __init__(self):
        self.request = Request(Endpoint.CONTACTS, Method.GET, {"count": True})

    def setResponse(self, response: Response):
        self.response = ContactsCount(response)


class GetContactsWithOffsetAndLimit(GenericTransaction):
    '''
    Retrieve contacts with offset and limit
    '''
    def __init__(self, offset: int, limit: int):
        self.request = Request(Endpoint.CONTACTS, Method.GET, {"offset": offset, "limit": limit})

    def setResponse(self, response: Response):
        self.response = Contacts(response)


class GetContactById(GenericTransaction):
    '''
    Retrieve contacts with offset and limit
    '''
    def __init__(self, id: int):
        self.request = Request(Endpoint.CONTACTS, Method.GET, {"id": id})

    def setResponse(self, response: Response):
        self.response = Contacts(response)


class AddContact(GenericTransaction):
    '''
    Retrieve contacts with offset and limit
    '''
    def __init__(self, newContactEntry):
        try:
            self.request = Request(Endpoint.CONTACTS, Method.POST, newContactEntry)
        except TransactionError as err:
            pass

    def setResponse(self, response: Response):
        self.response = AddedContactId(response)

class DeleteContactById(GenericTransaction):
    '''
    Delete contact with specified by Id
    '''
    def __init__(self, id: int):
        self.request = Request(Endpoint.CONTACTS, Method.DEL, {"id": id})

    def setResponse(self, response: Response):
        self.response = DeletedContact(response)
