#### Basics of pylabrad servers

You can write a server simply by subclassing the LabradServer class and using the `@setting` decorator

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
#### Servers acting as clients

Many servers need to make requests to other servers.  Each server has a 'client' object for this purpose:

```python
    @setting(15, key='s', returns='?')
    def get_registry_key(self, c, server_name):
        p = self.client.registry.packet()
        p.get(key)
        result = yield p.send()  # Always wait=False
        returnValue(result['get'])
```

Notice that servers always make asynchronous requests, so we must use yield to get the value of the Deferred.  We then must use returnValue to send the result back, just as if this were an inlineCallbacks method.
#### Setting decorator

The setting decorator takes a number of options.  The first, required option is the setting ID number.  The only requirement is that this must be a positive integer, and it must be unique within the server.  The second option is optional, and is the name of the setting to be advertized to the manager.  If left off, the name will be derived from the function name.  The remaining keyword options are the argument names and types, with the 'returns' keyword argument specifying the return type:

```python
    @setting(10, 'cd', path=['s', '*s', 'w'], returns='*s') # 'cd' is optional and redundant
    def chdir(self, c, path=None):  # Path can also be unspecified.
        '''Code goes here'''
```
Type tags can be specified as a string or a list of strings.  The setting decorator will inspect the method signature for default arguments, in which case it will generate additional type tags allowing the argument to be missing.

#### Contexts

The second argument to every setting function (after self) is the context, usually called `c`.  This allows the server to store state on a per-client basis.  It acts like a dictionary which the server implementation is allowed to store arbitrary keys.  It also has the attribute `c.ID` containing the ID of the client making the request.  There are two special methods that a server can override: `initContext(self, c)` and `expireContext(self, c)`.  These are called the first time a client uses a specific context, and when the context expires (usually because the client disconnected from the labrad manager).

#### Signals

LabRAD support signals.  These are messages sent by servers triggered by an external event, rather than as a response to a specific client request.  For instance, the data vault sends a signal to every listening client when a new file is created.  This allows e.g. the grapher to update its display without polling the server.  Signals are declared in pylabrad servers like so:

```python
from labrad.server import LabradServer, Signal, setting

class SignalTestServer(LabradServer):
    onNotification = Signal(1234, 'signal: test', 's')
    @setting(10, message='s')
    def notify_clients(self, c, message):
        self.onNotification(message)  # send the message to all listening clients

