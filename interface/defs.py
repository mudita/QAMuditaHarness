# Copyright (c) 2017-2021, Mudita Sp. z.o.o. All rights reserved.
# For licensing, see https://github.com/mudita/MuditaOS/LICENSE.md
from enum import Enum

endpoint = {
    "deviceInfo": 1,
    "update": 2,
    "filesystem": 3,
    "backup": 4,
    "restore": 5,
    "factory": 6,
    "contacts": 7,
    "messages": 8,
    "calllog": 9,
    "events": 10,
    "developerMode": 11,
    "bluetooth": 12,
    "usbSecurity": 13
}


class Endpoint(Enum):
    INVALID = 0
    DEVICEINFO = 1
    UPDATE = 2
    FILESYSTEM = 3
    BACKUP = 4
    RESTORE = 5
    FACTORY = 6
    CONTACTS = 7
    MESSAGES = 8
    CALLLOG = 9
    EVENTS = 10
    DEVELOPERMODE = 11
    BLUETOOTH = 12
    USBSECURITY = 13


method = {
    "get": 1,
    "post": 2,
    "put": 3,
    "del": 4
}


class Method(Enum):
    GET = 1
    POST = 2
    PUT = 3
    DEL = 4


status = {
    "OK": 200,
    "Accepted": 202,
    "NoContent": 204,
    "SeeOther": 303,
    "BadRequest": 400,
    "Forbidden": 403,
    "NotFound": 404,
    "NotAcceptable": 406,
    "InternalServerError": 500,
    "NotImplemented": 501,
}


class Status(Enum):
    OK = 200
    Accepted = 202
    NoContent = 204
    SeeOther = 303
    BadRequest = 400
    Forbidden = 403
    NotFound = 404
    NotAcceptable = 406
    InternalServerError = 500
    NotImplemented = 501


key_codes = {
    "left": ord('a'),
    "right": ord('d'),
    "up": ord('w'),
    "down": ord('s'),
    "enter": ord('\n'),
    "fnLeft": 11,
    "fnRight": 12,
    "volUp": 13,
    "volDown": 14,
    "torch": 15,
    "sliderUp": 16,
    "sliderMid": 18,
    "sliderDown": 17,
    "#": ord('#'),
    "*": ord('*'),
}

default_pin = [3, 3, 3, 3]

class SMSType(Enum):
    DRAFT = 0x01
    FAILED = 0x02
    INBOX = 0x04
    OUTBOX = 0x08
    QUEUED = 0x10
    INPUT = 0x12
    UNKNOWN = 0xFF
