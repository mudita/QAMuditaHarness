# Copyright (c) 2017-2021, Mudita Sp. z.o.o. All rights reserved.
# For licensing, see https://github.com/mudita/MuditaOS/LICENSE.md
import random

from . import utils
from . import log

from .utils import send_keystoke
from .utils import application_keypath
from .utils import send_char
from .utils import clear_last_char

from .interface import CDCSerial as serial

from .interface.error import TestError
from .interface.error import Error

from .interface.defs import key_codes
from .interface.defs import endpoint
from .interface.defs import method
from .interface.defs import default_pin


class Harness:
    connection = None
    is_echo_mode = False
    port_name = ''

    def __init__(self, port):
        self.port_name = port
        self.connection = serial.CDCSerial(port)

    @classmethod
    def from_detect(cls):
        '''
        Try to instantiate from first detected device.
        Do not use this method if you need >1 unique devices.
        '''
        found = serial.CDCSerial.find_Pures()
        if found:
            port = found[0]
            return cls(port)
        else:
            raise TestError(Error.PORT_NOT_FOUND)

    def get_connection(self):
        return self.connection

    def get_application_name(self):
        return self.connection.get_application_name()

    def unlock_usb(self):
        self.connection.usb_unlock()

    def lock_usb(self):
        self.connection.usb_lock()

    def is_phone_locked(self):
        return self.connection.is_phone_locked()


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
