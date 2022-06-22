from ..request import Request, Response
from ..interface.defs import Endpoint, Method
from .generic import GenericResponse, GenericTransaction


class ThreadsResponse(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.threads = self.response.body["entries"]
        self.totalCount = self.response.body["totalCount"]
        if "nextPage" in self.response.body:
            self.nextPage = self.response.body["nextPage"]


class ThreadByIdResponse(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.thread = self.response.body


class GetThreadsWithOffsetAndLimit(GenericTransaction):
    """
    Retrieve threads with offset and limit
    """

    def __init__(self, offset: int, limit: int):
        self.request = Request(Endpoint.MESSAGES, Method.GET,
                               {
                                   "category": "thread",
                                   "offset": offset,
                                   "limit": limit
                               })

    def setResponse(self, response: Response):
        self.response = ThreadsResponse(response)


class GetThreadById(GenericTransaction):
    """
    Retrieve thread by thread ID
    """

    def __init__(self, threadID: int):
        self.request = Request(Endpoint.MESSAGES, Method.GET,
                               {
                                   "category": "thread",
                                   "threadID": threadID
                               })

    def setResponse(self, response: Response):
        self.response = ThreadByIdResponse(response)


class MarkThreadAsUnread(GenericTransaction):
    """
    Mark thread as read/unread
    """

    def __init__(self, threadID: int, isUnread: bool):
        self.request = Request(Endpoint.MESSAGES, Method.GET,
                               {
                                   "category": "thread",
                                   "threadID": threadID,
                                   "isUnread": isUnread
                               })

    def setResponse(self, response: Response):
        self.response = GenericResponse(response)


class DeleteThreadById(GenericTransaction):
    """
    Delete thread specified by ID
    """

    def __init__(self, threadID: int):
        self.request = Request(Endpoint.MESSAGES, Method.DEL,
                               {
                                   "category": "thread",
                                   "threadID": threadID
                               })

    def setResponse(self, response: Response):
        self.response = GenericResponse(response)


class MessagesCountResponse(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.count = self.response.body["count"]


class MessagesResponse(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.messages = self.response.body["entries"]
        self.totalCount = self.response.body["totalCount"]
        if "nextPage" in self.response.body:
            self.nextPage = self.response.body["nextPage"]


class MessageByIdResponse(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = self.response.body


class AddMessageResponse(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = self.response.body


class GetMessagesCount(GenericTransaction):
    """
    Get the count of messages
    """

    def __init__(self):
        self.request = Request(Endpoint.MESSAGES, Method.GET,
                               {
                                   "category": "message",
                                   "count": True
                               })

    def setResponse(self, response: Response):
        self.response = MessagesCountResponse(response)


class GetMessagesWithOffsetAndLimit(GenericTransaction):
    """
    Retrieve messages with offset and limit
    """

    def __init__(self, offset: int, limit: int):
        self.request = Request(Endpoint.MESSAGES, Method.GET,
                               {
                                   "category": "message",
                                   "offset": offset,
                                   "limit": limit
                               })

    def setResponse(self, response: Response):
        self.response = MessagesResponse(response)


class GetMessageById(GenericTransaction):
    """
    Retrieve message by message ID
    """

    def __init__(self, messageID: int):
        self.request = Request(Endpoint.MESSAGES, Method.GET,
                               {
                                   "category": "message",
                                   "messageID": messageID
                               })

    def setResponse(self, response: Response):
        self.response = MessageByIdResponse(response)


class GetMessagesByThreadIdWithOffsetAndLimit(GenericTransaction):
    """
    Retrieve messages by thread ID with offset and limit
    """

    def __init__(self, threadID: int, offset: int, limit: int):
        self.request = Request(Endpoint.MESSAGES, Method.GET,
                               {
                                   "category": "message",
                                   "threadID": threadID,
                                   "offset": offset,
                                   "limit": limit
                               })

    def setResponse(self, response: Response):
        self.response = MessagesResponse(response)


class AddMessage(GenericTransaction):
    """
    Send a message to specified phone number
    """

    def __init__(self, number: str, messageBody: str):
        self.request = Request(Endpoint.MESSAGES, Method.POST,
                               {
                                   "category": "message",
                                   "number": number,
                                   "messageBody": messageBody
                               })

    def setResponse(self, response: Response):
        self.response = AddMessageResponse(response)


class DeleteMessageById(GenericTransaction):
    """
    Delete message specified by Id
    """

    def __init__(self, messageID: int):
        self.request = Request(Endpoint.MESSAGES, Method.DEL,
                               {
                                   "category": "message",
                                   "messageID": messageID
                               })

    def setResponse(self, response: Response):
        self.response = GenericResponse(response)


class TemplatesCountResponse(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.count = self.response.body["count"]


class TemplatesWithOffsetAndLimitResponse(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.templates = self.response.body["entries"]
        self.totalCount = self.response.body["totalCount"]
        self.nextPage = self.response.body["nextPage"]


class MessageTemplateResponse(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order = self.response.body["order"]
        self.lastUsedAt = self.response.body["lastUsedAt"]
        self.templateBody = self.response.body["templateBody"]
        self.templateID = self.response.body["templateID"]

class AddTemplateResponse(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.templateID = self.response.body["templateID"]


class GetTemplatesCount(GenericTransaction):
    """
    Get the count of templates
    """

    def __init__(self):
        self.request = Request(Endpoint.MESSAGES, Method.GET,
                               {
                                   "category": "template",
                                   "count": True
                               })

    def setResponse(self, response: Response):
        self.response = TemplatesCountResponse(response)


class GetTemplatesWithOffsetAndLimit(GenericTransaction):
    """
    Retrieve templates with offset and limit
    """

    def __init__(self, offset: int, limit: int):
        self.request = Request(Endpoint.MESSAGES, Method.GET,
                               {
                                   "category": "template",
                                   "offset": offset,
                                   "limit": limit
                               })

    def setResponse(self, response: Response):
        self.response = TemplatesWithOffsetAndLimitResponse(response)


class GetMessageTemplateById(GenericTransaction):
    """
    Retrieve template by message ID
    """

    def __init__(self, templateID: int):
        self.request = Request(Endpoint.MESSAGES, Method.GET,
                               {
                                   "category": "template",
                                   "templateID": templateID
                               })

    def setResponse(self, response: Response):
        self.response = MessageTemplateResponse(response)


class ChangeMessageTemplate(GenericTransaction):
    """
    Change message template
    """

    def __init__(self, templateID: int, templateBody: str):
        self.request = Request(Endpoint.MESSAGES, Method.PUT,
                               {
                                   "category": "template",
                                   "templateID": templateID,
                                   "templateBody": templateBody
                               })

    def setResponse(self, response: Response):
        self.response = GenericResponse(response)


class ChangeMessageTemplateOrder(GenericTransaction):
    """
    Change message template order
    """

    def __init__(self, templateID: int, order: int):
        self.request = Request(Endpoint.MESSAGES, Method.PUT,
                               {
                                   "category": "template",
                                   "templateID": templateID,
                                   "order": order
                               })

    def setResponse(self, response: Response):
        self.response = GenericResponse(response)


class AddMessageTemplate(GenericTransaction):
    """
    Add message template
    """

    def __init__(self, templateBody: str):
        self.request = Request(Endpoint.MESSAGES, Method.POST,
                               {
                                   "category": "template",
                                   "templateBody": templateBody
                               })

    def setResponse(self, response: Response):
        self.response = AddTemplateResponse(response)


class DeleteMessageTemplateById(GenericTransaction):
    """
    Delete message template specified by Id
    """

    def __init__(self, templateID: int):
        self.request = Request(Endpoint.MESSAGES, Method.DEL,
                               {
                                   "category": "template",
                                   "templateID": templateID
                               })

    def setResponse(self, response: Response):
        self.response = GenericResponse(response)
