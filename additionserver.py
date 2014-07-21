import time

from labrad.server import LabradServer, setting

class AdditionServer(LabradServer):
    name = "Addition Server"

    @setting(10, a='v[]', b='v[]', returns='v[]')
    def add(self, c, a, b):
        time.sleep(1)
        return a + b

__server__ = AdditionServer()

if __name__ == '__main__':
    from labrad import util
    util.runServer(__server__)
