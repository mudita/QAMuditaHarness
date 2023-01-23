from enum import IntEnum

from harness.interface.defs import Endpoint, Method
from harness.request import Request, Response

from .generic import GenericResponse, GenericTransaction


class DiagnosticsFileList(IntEnum):
    LOGS = (0,)
    CRASH_DUMPS = (1,)
    INVALID = 2


class DeviceDiagListInitResponse(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.response.body:
            self.files = []
            return
        self.files = self.response.body["files"]


class DeviceInfoInitResponse(GenericResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.diag_info = self.response.body


class GetDiagnosticFilesList(GenericTransaction):
    """
    Requests diagnostic files list based on type from device
    """

    def __init__(self, type: DiagnosticsFileList):
        self.request = Request(
            Endpoint.DEVICEINFO, Method.GET, {"fileList": type.value}
        )

    def setResponse(self, response: Response):
        self.response = DeviceDiagListInitResponse(response)


class GetDeviceInfo(GenericTransaction):
    """
    Requests device info
    """

    def __init__(self):
        self.request = Request(Endpoint.DEVICEINFO, Method.GET, {})

    def setResponse(self, response: Response):
        self.response = DeviceInfoInitResponse(response)
