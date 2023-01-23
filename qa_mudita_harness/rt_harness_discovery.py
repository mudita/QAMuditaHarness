import time

from . import log
from .harness import Harness
from .interface.error import Error, TestError
from .utils import Timeout

simulator_port = "simulator"


def get_harness_automatic(timeout, retry_time_s=1) -> Harness:
    """
    automatic harness connection discovery, polls for harness phone connection on uart
        timeout - time we wait for connection
        retry_time_s - time between open retries
    """
    harness = None

    # There is a period of time between the moment the device is detected and when it is ready
    # to accept commands. All data sent during this window will be lost, so wait for the time
    # defined here before sending anything.
    detection_to_readiness_time = 5

    log.debug(f"await for port {timeout}s")
    with Timeout.limit(seconds=timeout):
        while not harness:
            try:
                harness = Harness.from_detect()
            except TestError as e:
                if e.get_error_code() == Error.PORT_NOT_FOUND:
                    time.sleep(retry_time_s)
            if harness is not None:
                log.debug(
                    f"found port, waiting {detection_to_readiness_time}s for device to be ready"
                )
                time.sleep(detection_to_readiness_time)
    return harness


def get_harness_by_port_name(port: str, timeout, retry_time_s=1) -> Harness:
    """
    if port is named `simulator` then try to open simulator /tmp/purephone_pts_name
    else try uart specified
        port - port to open either /dev/... or `simulator`
        timeout - timeout to try to open port
        retry_time_s - time between open retries
    """
    assert "/dev" in port or simulator_port in port

    if simulator_port in port:
        file = None

        log.debug(f"await for port {timeout}s")
        with Timeout.limit(seconds=timeout):
            while not file:
                try:
                    file = open("/tmp/purephone_pts_name", "r")
                except FileNotFoundError:
                    time.sleep(retry_time_s)
        port = file.readline()
        if port.isascii():
            log.debug("found {} entry!".format(port))
        else:
            raise ValueError("not a valid sim pts entry!")
    return Harness(port)
