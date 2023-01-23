from ..harness import Harness
from ..request import Response

'''
GenericResponse based classes provide wrapper to get data via parameter i.e.
FsInitResponse provides us with:
    FsInitResponse.rxID
Which then is used in transfer.

GenericTransaction based class provides us with whole transaction of single Request->Response
and can be executed with harness provided.

Please see developer mode example:
    PhoneModeLock(False).run(harness)
'''


class GenericResponse:
    '''
    Generic response class - used to wrap Response and be a base to provide parameters with its children
    used for parsing
    '''
    response = None

    def __init__(self, resp):
        self.response = resp


class GenericTransaction:
    '''
    Generic transaction class represenging Request->Response execution
    used to provide transactions i.e. PhoneModeLock transaction
    '''
    def getRequest(self):
        return self.request

    def getResponse(self):
        return self.response

    def setResponse(self, response: Response):
        raise TypeError("Child class has to implement setResponse")

    def onRun(self, harness: Harness):
        '''
        Method to call before run - for children to be able to call before sth happened
        '''
        pass

    def run(self, harness: Harness):
        self.onRun(harness)
        ret = harness.request(self.request.endpoint, self.request.method, self.request.body)
        self.setResponse(ret.response)
        return self.getResponse()
