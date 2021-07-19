from .harness import Harness
from .interface.error import TestError, Error
from . import log
from .utils import Timeout
import time


def get_rt1051_harness(timeout):
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
                    time.sleep(1)
    return harness
