#### Direct interface with a server
```python
cxn = labrad.connect()
myServer = cxn.my_server
result = my_server.foo(args)
```

#### Use a "packet" to send multiple requests at once

```python
p = cxn.my_server.packet()
p.foo(args)
p.bar(args)
result = p.send() # This is a blocking call
answer_to_foo = result['foo']
answer_to_bar = result['bar']
```
`result` is a dictionary keyed by the name of each setting.  If you invoke the same setting multiple times in a single packet the result is a list.  Alternately, you can set your own keys for each request

```python
p = cxn.my_server.packet()
p.foo(args, key='banana')
p.foo(args, key='orange')
result = p.send()
answer_foo1 = result['banana']
answer_foo2 = result['orange']
```

#### Send a request to a server without waiting for the answer

```python
p = cxn.my_server.packet()
p.foo(args)
result_future = p.send(wait=False) # This is not a blocking call
<other code>
# Now we want to wait for the answer to our request.
# Once this call completes, we will be able to do
# result['foo'] to retrieve the result of our request.
result = result_future.wait()
print("result of foo is: ", result['foo']
```

#### Contexts

Each labrad request happens within a specific context.  Servers use that context to store specific information about the client such as their current working directory  (datavault, registry) or the currently selected GPIB device (any GPIB device server).  Each client gets its own default context, which is normally all you need.  To get a new context (for instance to avoid trampling over the working directory, or for keeping pipelined requests to the qubit sequencer separate):

```python
ctx = cxn.context()  # Returns a tuple like (0, 5)
p = cxn.my_server.packet(context=ctx)
p.foo(args)
p.send()
```

#### Signals

Labrad servers can send signals.  Signals are asynchronous notifications from servers that do not come as a reply to a particular request.  Each client must register to receive a particular signal in order for it to be delivered.  Setting up a client to receive a notification is a two step process:

```python
def signal_handler(message_ctx, data):
   print("Got signal in context %s with data: %s" % (message_ctx, data))

def set_listner(cxn, server, ctx=None):
    notification_ID = 4444
    cxn._backend.cxn.addListener(signal_handler, source=server.ID, context=ctx, ID=notification_ID)
    server.signal_name.notify_on_change(notification_ID, True, context=ctx) # True enables notification
```

The addListner call sets up the local client code so that when it receives a notification from a specific server with a specific ID and context to dispatch it to the registered function.  The notify_on_change call sends a message to the server telling it that we want to receive notifications, and that they should be send to use with the ID and context specified.  The ID (`4444` here) serves much the same purpose as a server's setting ID.  It is used to route each notification to the proper handler.  It can be anything, but it must be unique: a client can't use the same notification ID for two messages.

#### Debugging tips

## Next

[Writing servers](Writing-Servers.md)
