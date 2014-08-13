The LabRAD Node is a server that is used for starting and stopping other servers.

## Running the Node

The node is currently implemented as a Twisted plugin. As long as twisted.plugins.labrad_node is in your pythonpath, you can run the plugin like this:

    twistd -n labradnode

where -n means "don't daemonize" and `labradnode` is the name of the plugin. (Note that either installing pylabrad with setup.py or putting the labrad/ folder in your pythonpath is sufficient.) Running the node as a plugin is handy because if you restart the manager, it will automatically attempt to reconnect.

There is also a new script in the scripts folder of pylabrad, labradnode.py. All this does is the equivalent of the `twistd` command given earlier. This makes it easy to start the node without a command line (e.g. in Windows).

## Using the Node

Each node has a name--either the environment variable LABRADNODE or the system's hostname. 

You must point the node to the folder where your servers are stored. There is a folder in the registry for the node, `>> Nodes >> [node name]`, with the key "Directories", which is a list of directories (strings) that the node looks to for servers. (This registry directory may be created automatically when the node is first run with a given node name.)

The node is fairly self-explanatory to use; key settings are `available_servers`, `running_servers`, `start`, `stop`, `status`, etc.

## Modifying the Node

The node files are here:
* [The node itself](https://github.com/martinisgroup/pylabrad/blob/master/labrad/node/__init__.py) is in the labrad/node directory.
* [The part that makes it a plugin](https://github.com/martinisgroup/pylabrad/blob/master/twisted/plugins/labrad_node.py) is in the twisted/plugin directory.

The twisted plugin docs are [here](https://twistedmatrix.com/documents/current/core/howto/plugin.html).