# Copyright (c) 2017-2020, Mudita Sp. z.o.o. All rights reserved.
# For licensing, see https://github.com/mudita/MuditaOS/LICENSE.md
import time
import serial
import json
import logging
from enum import Enum
from random import randrange

from .defs import endpoint, method
from .error import TestError, Error, ComError
from dataclasses import dataclass
from inotify import adapters
from inotify.constants import IN_ATTRIB

inotify_logger = logging.getLogger(adapters.__name__)
inotify_logger.setLevel(logging.ERROR)
log = logging.getLogger(__name__)


class Keytype(Enum):
    long_press = 0
    short_press = 1


@dataclass
class Stats():
    start: int
    end: int

    def elapsed(self):
        return self.end - self.start


def timed(foo):
    def wrap(*args, **kwargs):
        start = time.time()
        ret = foo(*args, **kwargs)
        end = time.time()
        return [ret, Stats(start, end)]
    return wrap


class CDCSerial:
    def __init__(self, port_name, timeout=10):
        self.timeout = timeout
        self.body = ""
        self.header_length = 10
        self.port_name = port_name
        while timeout != 0:
            try:
                self.serial = serial.Serial(port_name, baudrate=115200, timeout=10)
                self.serial.flushInput()
                log.info(f"opened port {port_name}!")
                self.watch_port()
                break
            except (FileNotFoundError, serial.serialutil.SerialException) as err:
                log.error(f"can't open {port_name}, retrying...")
                time.sleep(1)
                self.timeout = self.timeout - 1
                if self.timeout == 0:
                    log.error(f"uart {port_name} not found - probably OS did not boot")
                    raise TestError(Error.PORT_NOT_FOUND)

    def watch_port(self):
        '''
        inotify in python uses epoll to check notifications
        set insignificant timeout of 0.01ms instead of 1s default
        '''
        self.watch = adapters.Inotify(block_duration_s=0.0)
        self.watch.add_watch(self.port_name, IN_ATTRIB)

    def watch_port_status(self):
        for event in self.watch.event_gen():
            if event is None:
                return
            (_, type_names, path, filename) = event
            log.debug(f"inotify {path}/{filename} event: {type_names}")
            raise TestError(Error.PURE_REBOOT)

    def watch_port_reboot(self, timeout=10):
        for event in self.watch.event_gen(timeout_s=timeout, yield_nones=False):
            (_, type_names, path, filename) = event
            log.debug(f"inotify {path}/{filename} event: {type_names}")
            return True
        return False

    def __del__(self):
        try:
            self.serial.close()
            log.info(f"closed port {self.serial.name}")
        except (serial.serialutil.SerialException, AttributeError):
            pass

    def __wrap_message(self, body):
        msg = {
            "endpoint": endpoint["developerMode"],
            "method": method["put"],
            "uuid": randrange(1, 100),
            "body": body
        }
        return msg

    def get_serial(self):
        return self.serial

    def __build_message(self, json_data):
        json_dump = json.dumps(json_data)
        return "#%09d%s" % (len(json_dump), json_dump)

    @timed
    def read(self, length):
        header = self.readRaw(length)
        payload_length = int(header[1:])
        result = self.readRaw(payload_length)
        return result

    def readRaw(self, length):
        data = self.serial.read(length).decode()
        data_len = len(data)
        if data_len == 0 and length != 0:
            raise ComError(f"Nothing read of requested {length}!")
        if data_len != length:
            raise ComError("Not enough data: {data_len} != {length} !")
        return data

    def get_timing(self):
        return [self.time_to_send, self.time_to_read]

    def write(self, msg, timeout=30):
        message = self.__build_message(msg)
        ignore, self.time_to_send = self.writeRaw(message)
        result, self.time_to_read = self.read(self.header_length)
        return json.loads(result)

    @timed
    def writeRaw(self, message, timeout=30):
        self.watch_port_status()
        to_write = message.encode()
        to_write_len = len(to_write)
        len_written = self.serial.write(message.encode())
        if len_written != to_write_len:
            raise ComError(f"Written {len_written} of {to_write_len}")
        self.serial.timeout = timeout

    def send_key_code(self, key_code, key_type=Keytype.short_press, wait=10):
        if key_type is Keytype.long_press:
            body = {"keyPressed": key_code, "state": 4}
        else:
            body = {"keyPressed": key_code, "state": 2}
        ret = self.write(self.__wrap_message(body), wait)
        time.sleep(0.3)
        return ret

    def enable_echo_mode(self):
        echoOnCmd = "UsbCdcEcho=ON"
        self.writeRaw(echoOnCmd)
        result = self.readRaw(len(echoOnCmd))
        log.info(f"received length: {len(result)}, result:{result}")
        ret = (result == echoOnCmd)
        return ret

    def disable_echo_mode(self):
        echoOffCmd = "UsbCdcEcho=OFF"
        self.writeRaw(echoOffCmd)
        result = self.readRaw(len(echoOffCmd))
        log.info(f"received length: {len(result)}, result:{result}")
        ret = (result == echoOffCmd)
        return ret

    def send_at(self, at_command, timeout, wait=10):
        body = {
            "AT": at_command + "\r",
            "timeout": timeout
        }

        ret = self.write(self.__wrap_message(body), timeout / 1000 + wait)
        log.info(f"at response {ret}")
        return ret["body"]["ATResponse"]

    def get_application_name(self):
        body = {
            "focus": True
        }

        ret = self.write(self.__wrap_message(body))
        return ret["body"]["focus"]

    def is_phone_locked(self):
        body = {
            "phoneLocked": True
        }

        ret = self.write(self.__wrap_message(body))
        return ret["body"]["phoneLocked"]

    @staticmethod
    def find_Pures() -> str:
        '''
        Return a list of unique paths to all the Mudita Pure phones found connected to the system
        '''
        import serial.tools.list_ports as list_ports
        return [_.device for _ in list_ports.comports() if _.manufacturer == 'Mudita' and _.product == 'Mudita Pure']

