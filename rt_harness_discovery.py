from .harness import Harness
from .interface.error import TestError, Error
from . import log
from .utils import Timeout
import time


simulator_port = 'simulator'


def get_harness_automatic(timeout, retry_time_s=1) -> Harness:
    '''
    automatic harness connection discovery, polls for harness phone connection on uart
        timeout - time we wait for connection
        retry_time_s - time between open retries
    '''
    harness = None
    timeout_started = time.time()

    with Timeout.limit(seconds=timeout):
        while not harness:
            try:
                harness = Harness.from_detect()
            except TestError as e:
                if e.get_error_code() == Error.PORT_NOT_FOUND:
                    log.debug(
                        f"waiting for a serial port… ({timeout- int(time.time() - timeout_started)})")
                    time.sleep(retry_time_s)
    return harness


def get_harness_by_port_name(port: str, timeout, retry_time_s=1) -> Harness:
    '''
    if port is named `simulator` then try to open simulator /tmp/purephone_pts_name
    else try uart specified
        port - port to open either /dev/... or `simulator`
        timeout - timeout to try to open port
        retry_time_s - time between open retries
    '''
    assert '/dev' in port or simulator_port in port
    timeout_started = time.time()

    if simulator_port in port:
        file = None
        with Timeout.limit(seconds=timeout):
            while not file:
                try:
                    file = open("/tmp/purephone_pts_name", "r")
                except FileNotFoundError:
                    log.info(
                        f"waiting for a simulator port… ({timeout- int(time.time() - timeout_started)})")
                    time.sleep(retry_time_s)
        port = file.readline()
        if port.isascii():
            log.debug("found {} entry!".format(port))
        else:
            raise ValueError("not a valid sim pts entry!")
    return Harness(port)
