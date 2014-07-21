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
Your can find the script in [synchronousclient_1.py](synchronousclient_1.py),
which is reproduced here:

```python
import labrad
import time

def square_numbers(cxn, numbers):
    ss = cxn.squaring_server
    t_start = time.time()
    print("Starting synchronous requests...")
    for n in numbers:
        square = ss.square(n)
        print("%f**2 = %f"%(n, square))
    t_total = time.time() - t_start
    print("Finished %d requests after %f seconds."%(len(numbers), t_total))
```

In the interactive session, import it and run the `square_numbers` function:

```python
import synchronousclient_1 as sc1
sc1.square_numbers(cxn, (1, 2))
```

You should see the following output

```python
>>> Starting synchronous requests...
>>> 1.000000**2 = 1.000000
>>> 2.000000**2 = 4.000000
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
Import [synchronousclient_2.py](synchronousclient_2.py) and run its `square_and_add` function.
Here's a copy/paste of synchronousclient_2.py:

```python
import labrad
import time

def square_and_add(cxn, square_me, x, y):
    ss = cxn.squaring_server
    ads = cxn.addition_server
    t_start = time.time()
    
    print("Sending request to Squaring Server")
    squared = ss.square(square_me)
    t_square = time.time()
    print("Got result %f**2 = %f after %f seconds"%\
        (square_me, squared, t_square - t_start))
    
    print("Sending request to Addition Server")
    summed = ads.add(x, y)
    t_summed = time.time()
    print("Got result %d + %d = %d after %f seconds"%\
        (x, y, summed, t_summed - t_square))
    t_total = t_summed - t_start
    print("Total time taken = %f seconds."%(t_total,))
    return squared, summed
```

In your python shell, type the following:

```python
import synchronousclient_2 as sc2
sc2.square_and_add(cxn, 1.414, 2, 5)
```

You should see output something like this:

```python
Sending request to Squaring Server
Got result 1.414**2 = 1.99 after 2.004 seconds
Sending request to Addition Server
Got result 2 + 5 = 7 after 1.004 seconds
Total time taken = 3.008 seconds.
>>> (1.999, 7.0)
```

If you look in the Addition Server's code, you'll see that the `add`
setting has a 1 second delay to simulate time time needed by an intense
computation.
Combined with the 2 seconds needed by the squaring server, this gives a
total 3 seconds needed for our `square_and_add` function.

In python, each line of code must complete before the next one can
execute.
In [synchronousclient_2](synchronousclient_2.py), the line

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

Consider the order of events in [synchronousclient_2](synchronousclient_2.py).
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
In pylabrad, this is easy.
We tell pylabrad to not wait for the result of a server request by setting
`wait=False` in the request:

```python
request = squaring_server.square(1.414, wait=False)
```

This makes a request to the `square` setting but does not wait for the
result before going to the next line of code.
Try it yourself in the interactive session.
You'll notice that the line completes immediately.
Since the line completes immediately, but we know that the `square`
setting takes 2 seconds to complete, the value of `request` must not
actually be the result of `1.414**2`.
In fact, the result of a LabRAD setting called with `wait=False` is an
object which represents the data to be returned at some point in the
future.
Try typing

```python
type(request)
```

at the interactive session to see for yourself.
You'll see that `request` is a `labrad.backend.Future`.
Behind the scenes, the part of pylabrad which deals with network
communication waits for the data from the squaring Server to come
back, and when it does, it updates the `request` object with the
returned data.
To explicitly wait for this data you can call `.wait()` on `response`.

```python
squared = response.wait()
```

The `wait()` call blocks until the result is received from the Squaring Server,
at which point it returns that result and stores it in `squared`.
Objects representing results which may come later are called "futures" in
computer programming (hence the name `labrad.backend.Future`).

The `.wait()` call is blocking.
When we call `.wait` on a future, python will not go to the next line
until the result of the future is available.

We can use futures to make our two requests to the Squaring and Addition
servers run faster.
We ask the Squaring Server to run `square`, using `wait=False`.
Then, while that result is being computed, we can immediately ask the
Addition Server to run `add`, again with `wait=False`.
Both servers will start cranking away at their respective computations.
We then call `.wait()` on the two resulting futures in any order to
collect the results.
The code to do this is in [asynchronousclient_1.py](asynchronousclient_1.py),
which is reproduced here:

```python
import labrad
import time

def square_and_add(cxn, square_me, x, y):
    ss = cxn.squaring_server
    ads = cxn.addition_server
    t_start = time.time()
    print("Sending request to Squaring Server")
    squared_future = ss.square(square_me, wait=False)
    print("Sending request to Addition Server")
    summed_future = ads.add(x, y, wait=False)
    print("Waiting for results...")
    squared = squared_future.wait()
    summed = summed_future.wait()
    print("done")
    t_total = time.time() - t_start
    print("%f**2 = %f"%(square_me, squared))
    print("%d + %d = %d"%(x, y, summed))
    print("Total time taken = %f seconds."%(t_total))
    return squared, summed
```

To run it, in the interactive session, do this:

```python
import asynchronousclient_1 as ac1
ac1.square_and_add(cxn, 1.414, 2, 5)
```

You should see output like

```python
Sending request to Squaring Server
Sending request to Addition Server
Waiting for results...
done
1.414000**2 = 16.000000
3 + 6 = 9
Total time taken = 2.005274 seconds.
>>> (2.0, 7.0)
```

Note that the total time is the longest of the two requests we made.
This illustrates the benefit of asynchronous (parallel) behavior:
the time for the computation is the time of the longest part, rather than the
sum of all the parts.

### Asynchronous Servers

Needs to be written.
