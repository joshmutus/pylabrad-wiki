You can write a server simply by subclassing the LabradServer class and using the @setting decorator

```python
from labrad.server import LabradServer, setting
from twisted.internet.defer import inlineCallbacks, returnValue

class MyServer(LabradServer)
    name = "My Server"    # Will be labrad name of server
    
    @inlineCallbacks
    def initServer(self):  # Do initialization here
        pass

    @setting(10, data='?', returns='b'):
    def is_true(self, c, data):
        return bool(data)

__server__ = MyServer()

if __name__ == '__main__':
    from labrad import util
    util.runServer(__server__)
```

Many servers need to make requests to other servers.  Each server has a 'client' object for this purpose:

```python
    @setting(15, key='s', returns='?')
    def get_registry_key(self, c, server_name):
        p = self.client.registry.packet()
        p.get(key)
        result = yield p.send()  # Always wait=False
        returnValue(result['get'])
```

Notice that servers always make asynchronous requests, so we must use yield to get the value of the Future.  We then must use returnValue to send the result back, just as if this were an inlineCallbacks method.