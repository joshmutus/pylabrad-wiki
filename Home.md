# pylabrad: A Python interface to LabRAD

pylabrad is a python package to provide an interface to the LabRAD system, a remote procedure call protocol designed for scientific datataking.

## Required Packages

To get started with pylabrad, you'll first need to install some software:

1. **Python** version 2.7 or greater (Stay tuned for Python 3.x support). Python is, in our opinion, one of the best programming languages out there. It's easy to learn and easy to use, and helps you get more done faster.
1. **Twisted** version 2.5 or greater. Download it [here](https://twistedmatrix.com/trac/). Twisted is a networking framework for python that we use to handle all the low-level networking stuff for pylabrad.
1. **pylabrad**. Install from source, or use pip to get it from PyPI.

## Python Add-ons

We also recommend souping up your python installation with a few other packages to enhance the experience of using python/pylabrad:

1. **IPython**. A replacement for the python shell that provides loads of great features. Our favorite is definitely tab-completion, which makes controlling labrad from the command line a cinch. We'll show examples of IPython usage in the rest of this tutorial.
1. **Numpy/Scipy**. These packages provide incredible numerical and scientific computing capability for python. Numpy array objects can be used in pylabrad to accelerate operations on numeric data. Also check out the SciPy website for links to other great software for scientific computing with python.
1. **matplotlib**. Very nice, MATLAB-style plotting for python.

## Getting Started

As a first step, look through the basic LabRAD tutorial. This will help you get the LabRAD manager up and running, which you need to do before continuing. Also, make sure you've installed the software above. Then we're ready to go.

Fire up your python shell, and import the labrad package:
```python
>>> import labrad
```

Now we can establish a connection to the LabRAD manager. We need to know where the manager is running in order to connect to it. Let's suppose that the manager is running on your local machine, then you would type:
```python
>>> cxn = labrad.connect('localhost') 
```

(We can set up pylabrad with defaults so that we don't need to specify the hostname every time we connect; see [ConfiguringDefaults] for more information.)
This command created a connection to the LabRAD system, and assigned the connection object to a variable called `cxn`. This object is our gateway to LabRAD. Most of the objects in pylabrad have informative string representations, which will be printed out when that object is entered by itself on the command line:
```python
>>> cxn
LabRAD Client: 'Python Client' on localhost:7682

Available servers:
    manager
    registry
```

The list shows the servers that are logged in to LabRAD and available for us to talk to them. You may see more servers in the list, depending on what is logged in, but you will see at least the manager and registry. These available servers can be accessed as attributes of the connection object, or looked up by name like dictionary entries:
```python
>>> cxn['manager']; cxn.manager
LabRAD Server: manager (ID=1)

The LabRAD Manager handles the interactions between parts of the LabRAD system.

Settings:
    blacklist
    convert_units
    data_to_string
    expire_context
    help
    lookup
    lr_settings
    notify_on_connect
    notify_on_disconnect
    s__notify_on_context_expiration
    s__register_setting
    s__start_serving
    s__unregister_setting
    servers
    string_to_data
    whitelist
```

Finally we can talk to a specific setting on the server. The `data_to_string` setting will take any valid LabRAD data and return a string version of it, somewhat like python does with it's `repr` and `str` functions. We can get information about this setting by entering it, just like connection and server objects:
```python
>>> cxn.manager['data_to_string']; cxn.manager.data_to_string
LabRAD Setting: manager.pretty_print (ID=12345)

Returns a string representation of the data sent to it.

Accepts:

Returns:
    s

This setting is primarily meant for test-purposes.
```

This gives some documentation provided by the creator of the server, and also tells us what data types the setting accepts and returns. In the case of the data-to-string setting, any type is acceptable, so the Accepts list is empty. Whatever we pass in, a string will be returned. The setting can be called just like any other method on a python object, except that behind the scenes a request is made over the network to the server where the request is executed and the response comes back. Let's try this out:
```python
>>> cxn.manager.data_to_string([(1, 'This'), (2, 'is'), (3, 'a'), (4, 'test.')])
"[(+1, 'This'), (+2, 'is'), (+3, 'a'), (+4, 'test.')]"
```

Congratulations! You now know how to connect to LabRAD from python, find servers and settings, get information about them, and call them over the network. Using just these tools, you should be able to browse and communicate with your entire LabRAD network.