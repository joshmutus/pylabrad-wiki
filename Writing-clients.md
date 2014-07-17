#### Direct interface with a server
```python
cxn = labrad.connect()
myServer = cxn.my_server
result = my_server.foo(args)
```

#### Send multiple requests at once

```python
p = cxn.my_server.packet()
p.foo(args)
p.bar(args)
result = p.send() # This is a blocking call
answer_to_foo = result['foo']
answer_to_bar = result['bar']
```
You can set your own keys for each request

```python
p = cxn.my_server.packet()
p.foo(args, key='banana')
result = p.send()
answer_foo = result['banana']
```

#### Send a request to a server without waiting for the answer

```python
p = cxn.my_server.packet()
p.foo(args)
result = p.send(wait=False) # This is not a blocking call
<other code>
# Now we want to wait for the answer to our request.
# Once this call completes, we will be able to do
# result['foo'] to retrieve the result of our request.
result.wait() #XXX Is this right?
```

#### Contexts

Each labrad request happens within a specific context.  Servers use that context to store specific information about the client such as their current working directory  (datavault, registry) or the currently selected GPIB device (any GPIB device server).  Each client gets its own default context, which is normally all you need.  To get a new context (for instance to avoid trampling over the working directory, or for keeping pipelined requests to the qubit sequencer separate):

```python
ctx = cxn.context()  # Returns a tuple like (0, 5)
p = cxn.my_server.packet(context=ctx)
p.foo(args)
p.send()
```

#### Debugging tips

