import time

from labrad.server import LabradServer, setting

class SquaringServer(LabradServer):
    name = "Squaring Server"

    @setting(10, data='v[]', returns='v[]')
    def square(self, c, data):
        time.sleep(2)
        return data**2

__server__ = SquaringServer()

if __name__ == '__main__':
    from labrad import util
    util.runServer(__server__)
