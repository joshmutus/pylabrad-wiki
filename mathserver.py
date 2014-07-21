from labrad.server import LabradServer, setting
from twisted.internet.defer import returnValue

class MathServer(LabradServer):
    name = "Math Server"

    @setting(10, x='v[]', y='v[]', returns='v[]')
    def add(self, context, x, y):
        addition_server = self.client.addition_server
        result = yield addition_server.add(x, y)
        returnValue(result)

    @setting(0, data='v[]', returns='v[]')
    def square(self, context, data):
        squaring_server = self.client.squaring_server
        result = yield squaring_server.square(data)
        returnValue(result)

__server__ = MathServer()

if __name__ == '__main__':
    from labrad import util
    util.runServer(__server__)
