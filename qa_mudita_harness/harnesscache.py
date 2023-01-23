from . import log
from .api.developermode import PhoneModeLock
from .api.update import PhoneReboot, Reboot
from .harness import Harness
from .interface.error import ComError
from .rt_harness_discovery import get_harness_automatic, get_harness_by_port_name
from .utils import Timeout


class HarnessCache:
    '''
    harness session cache, to be used to:
        - create phone harness session
        - reset phone and create session
    '''
    harness: Harness = None

    @classmethod
    def cached(cls) -> bool:
        return True if cls.harness is not None else False

    @classmethod
    def is_operational(cls) -> bool:
        '''
        Check with timeout if endpoint is initialized by sending request that we are
        sure that exists and will have response
        '''
        # Timeout which is a max value to request data, it should happen in few seconds
        operational_timeout = 305
        if cls.harness is None:
            raise ValueError("No harness in cache")
        testbody = {"ui": True, "getWindow": True}
        result = None
        with Timeout.limit(seconds=operational_timeout):
            while not result:
                try:
                    result = cls.harness.endpoint_request("developerMode", "get", testbody)
                    return True
                except (ValueError, ComError):
                    log.info("Endpoints not ready..")
                    return False

    @classmethod
    def get(cls, port: str, timeout: int, retry_time_s: int, retries=1) -> Harness:
        '''
        depending on `port` get either selected port or discover pure automatically
        '''
        cls.timeout = timeout
        cls.retry_time_s = retry_time_s
        cls.port = port

        with Timeout.limit(seconds=timeout):
            while retries > 0:
                retries = retries - 1
                if port is None:
                    log.info("no port provided! trying automatic detection")
                    HarnessCache.harness = get_harness_automatic(cls.timeout, cls.retry_time_s)
                else:
                    log.info(f"port provided {port}")
                    HarnessCache.harness = get_harness_by_port_name(cls.port, cls.timeout, cls.retry_time_s)
                if HarnessCache.is_operational() is not True:
                    cls.harness = None
                    if retries == 0:
                        raise ValueError("harness not ready for use")
                else:
                    break
                import time
                time.sleep(cls.retry_time_s)
        if cls.harness is None:
            raise ValueError("port not found!")
        return cls.harness

    @classmethod
    def reset_phone(cls, reboot_cause: Reboot, reboot_time=6 * 60) -> Harness:
        '''
        Reset the phone flow:
            * reboot_time - time we wait till we say that reboot failed = 6 min default
            * time_to_reboot - time we wait till phone accepts reboot request and closes itself = 60s default
            * reboot_cause - we can reboot to updater, or any other selected in Reboot enum
        '''
        time_to_reboot = 60
        if cls.harness is None:
            raise ValueError("No harness in cache")

        PhoneReboot(reboot_cause).run(cls.harness)
        if not cls.harness.connection.watch_port_reboot(time_to_reboot):
            raise ValueError(f"Phone not rebooted in {reboot_time}")
        cls.harness = cls.get(cls.port, reboot_time, retry_time_s=1, retries=30)

        if not cls.harness.is_phone_locked():
            cls.harness.unlock_phone()
        PhoneModeLock(cls.harness.is_phone_mode_locked()).run(cls.harness)

        return cls.harness
