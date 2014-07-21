WARNING: This example has not actually been tested yet, and needs significant editin before it can be considered anywhere near complete -DTS

### Purpose

In this HOWTO, we investigate asynchronous behavior in pylabrad servers and
clients.

### Synchronous client

We begin with an example server, [the Squaring Server](squaringserver.py).
The Squaring Server has exactly one method, `square`, which computes the
square of a number and returns the result.
To simulate a long processor bound computation, we have inserted a time
delay into the `square` setting.
With the LabRAD manager running, fire up the Squaring Server on your machine.
Then, from the examples directory, start a python shell.
In the interactive shell, type:

```python
import labrad
cxn = labrad.connect()
ss = cxn.squaring_server
ss.square(1.414)
>>> 1.999...
```

You will have noted that when you hit `ENTER` on the `ss.square(1.414)`
line, there is an approximately 2 second delay before the command
finishes and the result comes back.
This is due to the 2 second delay in the `square` setting.
Now we will ask the server to square two numbers, one after the other.
This time we write our commands as a script.
Your can find the script in [synchronous-client-1](synchronous-client-1.py),
which is reproduced here:

```python
import labrad
import time

def square_numbers(cxn, numbers):
    ss = cxn.squaring_server
    t_start = time.clock()
    print("Starting synchronous requests...")
    for n in numbers:
        square = ss.square(n)
        print("%f**2 = %f"%(n, square))
    t_total = time.clock() - t_start
    print("Finished %d requests after %f seconds."%(len(numbers), t_total))
```

In the interactive session, import it and run the `square_numbers` function:

```python
import synchronous-client-1 as sc1
sc1.square_numbers(cxn, (1, 2))
```

You should see the following output

```python
>>> Starting synchronous requests...
>>> 1**2 = 1.0
>>> 2**2 = 2.0
>>> Finished 2 requests after 4.0 seconds.
```

Each `square` call on the Squaring Server takes 2 seconds, so our client
function, which invokes `square` twice, takes 4 seconds to run.
This is an example of "synchronous" behaviour: one task must finish
before the next can begin.
With the squaring operation, this is more or less unavoidable.
Squaring a number requires using a limited physical resource, the CPU.
While the CPU is busy squaring a number, there's no way for it to
simultaneously square another number (we're pretending for the moment
that your computer has only one processor core).

Operations, like number squaring, for which the resource bottleneck is
the local hardware (ie. the CPU) are called "CPU bound".
When you have a CPU bound operation (and only one core available) you
can't do anything to get work done faster.
You've got one CPU and only one operation can use it at a time.

Now suppose we have an [Addition Server](additionserver.py), whose only
setting, `add`, computes the sum of two numbers.
Like the `square` setting on the Squaring Server, `add` takes a bit of
time to complete.
Let's see what happens if we try to get both the Squaring Server and the
Addition Server to serve requests at the same time.
Fire up the Addition Server on your local machine.
Import the synchronous-client-2.py and run its `square_and_add` function.
Here's synchronous-client-2.py:

```python
import labrad
import time

def square_and_add(cxn, square_me, x, y):
    ss = cxn.squaring_server
    as = cxn.addition_server
    t_start = time.clock()
    print("Sending request to Squaring Server")
    squared = ss.square(square_me)
    print("Sending request to Addition Server")
    summed = as.add(x, y)
    t_total = time.clock() - t_start
    print("Time taken = %f seconds."%(len(numbers), t_total))
    return squared, summed
```

In your python shell, type the following:

```python
import synchronous-client-2 as sc2
sc2.square_and_add(cxn, 1.414, 2, 5)
```

You shoud see output something like this:

```python
>>> Finished after 3.0 seconds
```

If you look in the Addition Server's code, you'll see that the `add`
setting has a 1 second delay to simulate time time needed by an intense
computation.
Combined with the 2 seconds needed by the squaring server, this gives a
total 3 seconds needed for our `square_and_add` function.

Consider the order of events in synchronous-client-2.
First, we ask the Squaring Server to square 1.414.
The Squaring server receives our request, precesses it over a period of 2
seconds, and then sends the result back to the client (our local python
shell).
During this time, the Addition Server is doing absolutely nothing.
We send our request to the Addition Server only after we get a response
from the Squaring Server.
Suppose the Squaring and Addition servers were on two different
computers.
In that case, waiting for the Squaring Server to to respond before
sending a request to the Addition Server, makes no sense.
The answer to "2+5" has nothing to do with the result of 1.414**2,
so we might as well get both computations started at the same time.

In python, each line of code must complete before the next one can
execute.
In synchronous-client-2, the line

```python
squared = ss.square(square_me)
```

has to finish before the subsequent line invokes the Addition Server.
Calls like this, which require some computation to finish before the
program can move on, are called "blocking".
In other words, invoking and waiting for the Squaring Server "blocks" the
program from moving forward.
To be more efficient, we need to send off our request to the Squaring
Server and _not wait_ for the result before sending our request to the
Addition Server.

### Asynchronous client

pylabrad makes this easy, for example:

```python
response = squaring_server.square(1.414, wait=False)
```

This makes a request to the `square` setting but does not wait for the
result before going to the next line of code.
Try it yourself in the interactive session.
You'll notice that the line completes immediately.
Since the line completes immediately, but we know that the `square`
setting takes 2 seconds to complete, the value of `response` must not
actually be the result of `1.414**2`.
In fact, the result of a LabRAD setting called with `wait=False` is an
object which represents the data to be returned at some point in the
future.
Try typing

```python
type(response)
```

at the interactive session to see for yourself.
Behind the scenes, the part of pylabrad which deals with network
communication waits for the response from the squaring Server to come
back, and when it does, it updates the `response` object with the
returned data.
To explicitly wait for this data you can call `.wait()` on `response`.

```python
squared = response.wait()
```

Once the `wait()` call finishes, we are guaranteed that the expected data
has been stored as `squared`.
Objects representing results which may come later are called "futures" in
computer programming.

The `.wait()` call is blocking.
When we call `.wait` on a future, python will not go to the next line
until the result of the future is available.

We can use futures to make our two requests to the Squaring and Addition
servers run faster.
We ask the Squaring Server to run `square`, using `wait=False`.
Then, while that result is being computed, we can immediately ask the
Addition Server to run `add`, again with `wait=False`.
Both servers will stark cranking away at their respective computations.
We then call `.wait()` on the two resulting futures in any order to
collect the results.
The code to do tihs is in `asynchronous-client-1.py`, which is reproduced
here:

```python
import labrad
import time

def square_and_add(cxn, square_me, x, y):
    ss = cxn.squaring_server
    as = cxn.addition_server
    t_start = time.clock()
    print("Sending request to Squaring Server")
    squared_future = ss.square(square_me, wait=False)
    print("Sending request to Addition Server")
    summed_future = as.add(x, y, wait=False)
    for future in [squared_future, summed_future]:
        future.wait()
    t_total = time.clock() - t_start
    print("Time taken = %f seconds."%(len(numbers), t_total))
    # XXX Fix semantics here, which are definitely wrong.
    return squared, summed
```

To run it, in the interactive session, just do this

```python
import asynchronous-client-1 as ac1
result = ac1.square_and_add(1.414, 2, 5)
# XXX Again, fix semantics
```

This concludes the section on asynchronous behaviour in clients.
Next, we will show how to handle asynchronous behaviour in servers.

### Asynchronous Servers

Needs to be written.