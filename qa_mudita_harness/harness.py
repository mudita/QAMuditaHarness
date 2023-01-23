# Copyright (c) 2017-2021, Mudita Sp. z.o.o. All rights reserved.
# For licensing, see https://github.com/mudita/MuditaOS/LICENSE.md
import random

from . import log, utils
from .interface import CDCSerial as serial
from .interface.defs import Endpoint, Method, default_pin, endpoint, key_codes, method
from .interface.error import Error, TestError
from .request import Request, Transaction
from .utils import application_keypath, clear_last_char, send_char, send_keystoke


class Harness:
    '''
    harness class
    WARN: please see that variables below are not class local
    '''
    is_echo_mode = False
    port_name = ''

    def __init__(self, port):
        self.port_name = port
        self.connection = serial.CDCSerial(port)
        self.phone_mode_lock = False

    @classmethod
    def from_detect(cls):
        '''
        Try to instantiate from first detected device.
        Do not use this method if you need >1 unique devices.
        '''
        found = serial.CDCSerial.find_Devices()
        if found:
            port = found[0]
            return cls(port)
        else:
            raise TestError(Error.PORT_NOT_FOUND)

    def get_connection(self):
        return self.connection

    def set_connection(self, connection):
        Harness.connection = connection
        self.connection = connection

    def get_application_name(self):
        return self.connection.get_application_name()

    def is_phone_locked(self):
        return self.connection.is_phone_locked()

    def set_phone_mode_lock_state(self, enabled: bool):
        self.phone_mode_lock = enabled

    def is_phone_mode_locked(self):
        return self.phone_mode_lock

    def enter_passcode(self, pin=default_pin):
        utils.validate_pin(pin)
        if self.connection.is_phone_locked():
            self.connection.send_key_code(key_codes["enter"])
            self.connection.send_key_code(key_codes["#"])
            for digit in pin:
                self.connection.send_key_code(digit)

    def lock_phone(self):
        if not self.is_phone_locked():
            if not self.get_application_name() == "ApplicationDesktop":
                self.return_to_home_screen()
            self.connection.send_key_code(key_codes["#"], serial.Keytype.long_press)
            log.info("Phone locked")
        else:
            log.info("Phone already locked")

    def unlock_phone(self):
        if self.is_phone_locked():
            self.enter_passcode()
            log.info("Phone unlocked")
        else:
            log.info("Phone already unlocked")

    def with_phone_unlocked(self, func):
        if self.is_phone_locked():
            self.unlock_phone()

        func(self.connection)

    def return_to_last_screen(self):
        self.connection.send_key_code(key_codes["fnRight"])

    def return_to_home_screen(self):
        self.connection.send_key_code(key_codes["fnRight"], serial.Keytype.long_press)

    def connection_echo_mode_on(self):
        if self.connection.enable_echo_mode():
            self.is_echo_mode = True

    def connection_echo_mode_off(self):
        if self.connection.disable_echo_mode():
            self.is_echo_mode = False

    def open_application(self, app):
        send_keystoke(application_keypath[app], self.connection)

    def send_text(self, text: str):
        clear_last_char()
        for letter in text:
            try:
                send_char(letter, self.connection)
            except KeyError as e:
                available = ' '.join((f"'{_}'" for _ in utils.keymap.keys()))
                raise LookupError(f"Character {e} not present in the keymap\nAvailable characters: {available}")

    def send_number(self, number: str):
        utils.send_number(number, self.connection)

    def request(self, endpoint: Endpoint, method: Method, data: dict) -> Transaction:
        '''
        sends data to device and gets response
        the same as endpoint_request except:
            - works on types
            - throws in case of error
            - provides execution time
        use example:
        ```
            body = {"txID": txID, "chunkNo": chunkNo, "data": data}
            ret = harness.request(Endpoint.FILESYSTEM, Method.PUT, body)
            assert ret.response.body["txID"] != 0
        ```
        '''
        t = Transaction(Request(endpoint.value, method.value, data, random.randint(1, 32000)))
        t.accept(self.connection.write(t.request.to_dict()))
        r, w = self.connection.get_timing()
        r = r.elapsed()
        w = w.elapsed()
        t.set_elapsed(r, w)
        return t

    def endpoint_request(self, ep_name: str, met: str, body: dict) -> dict:
        ret = self.connection.write({
            "endpoint": endpoint[ep_name],
            "method": method[met],
            "uuid": random.randint(1, 32000),
            "body": body
        })
        return ret

    def turn_phone_off(self):
        log.info("Turning phone off...")
        app_desktop = "ApplicationDesktop"
        end_loop_counter = 10

        while not self.get_application_name() == app_desktop:
            if not end_loop_counter > 0:
                raise LookupError("Filed to switch to {}".format(app_desktop))
            log.info("Not on the Application Desktop, fnRight.")
            self.connection.send_key_code(key_codes["fnRight"], serial.Keytype.long_press)
            end_loop_counter -=  1

        self.connection.send_key_code(key_codes["fnRight"], serial.Keytype.long_press)
        self.connection.send_key_code(key_codes["right"])
        self.connection.send_key_code(key_codes["enter"])

    def set_tethering_state(self, enabled: bool):
        state = 'on' if enabled else 'off'
        body = {"tethering": state}
        log.info(f"Set tethering state to: {state}")
        return self.endpoint_request("developerMode", "put", body)

    def press_fun_left(self):
        self.connection.send_key_code(key_codes["fnLeft"])

    def press_fun_right(self):
        self.connection.send_key_code(key_codes["fnRight"])

    def press_fun_center(self):
        self.connection.send_key_code(key_codes["enter"])

    def press_nav_left(self):
        self.connection.send_key_code(key_codes["left"])

    def press_nav_right(self):
        self.connection.send_key_code(key_codes["right"])

    def press_nav_up(self):
        self.connection.send_key_code(key_codes["up"])

    def press_nav_down(self):
        self.connection.send_key_code(key_codes["down"])
