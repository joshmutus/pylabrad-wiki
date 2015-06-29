### How to emit a signal in a server
```python
    #Import Signal class
    from labrad.server import Signal

    # Create a LabRAD Signal object.
    onEvent = Signal( ID, signal_name, data_type)

    # e.g. ID = 543617.  The ID can be any number between X and XX
    # The ID number can not have a leading 0.

    # signal_name = 'signal: interesting information acquired'
    # This signal name is not trivial, it is what the client uses to connect to the 
    #signal in this instance the client would call 
    #server.signal__interesting_information_acquired() note the parsing of : and 
    #spaces.
    # data_type = 'i' for integer data.  These are the LabRAD data types 
    #(see link below for labrad data types).

    # Note onEvent Signal must be instantiated as a global class variable, i.e

    class ourserver( LabradServer):
        onEvent = ...
        ...
        def initServer(self):
            ...
```


### A simple example of a server emitting a signal

```python
    """
    ### BEGIN NODE INFO
    [info]
    name = Emitter Server
    version = 1.0
    description = 
    instancename = EmitterServer

    [startup]
    cmdline = %PYTHON% %FILE%
    timeout = 20

    [shutdown]
    message = 987654321
    timeout = 20
    ### END NODE INFO
    """

    from labrad.server import LabradServer, setting, Signal
    from twisted.internet import reactor
    from twisted.internet.defer import inlineCallbacks
    import labrad

    class EmitterServer(LabradServer):

        """
        Basic Emitter Server
        """
        name = 'Emitter Server'
    
        onEvent = Signal(123456, 'signal: emitted signal', 's')
        #This is the Signal to be emitted with ID# 123456 the name for the 
        #client to call is signal__emitted_signal and the labrad type is string
        
        @setting(1, 'Emit Signal', returns='')
        def emitSignal(self, c):
        #function that will onEvent to send signal to listeners
            self.onEvent('Output!')
            #sends signal
        
    if __name__ == "__main__":
        from labrad import util
        util.runServer(EmitterServer())
```

### How to receive a signal in a simple client

Now lets create a client that will listen for the string signal from the previous example (note this follows the writing GUI clients format closely and it may be beneficial to finish the GUI client tutorial prior to this tutorial)
```python
    from twisted.internet.defer import inlineCallbacks
    from PyQt4 import QtGui

    class recieverWidget(QtGui.QWidget):

        ID = 654321
    #this is an ID for the client to register to the server

        def __init__(self, reactor, parent=None):
            super(recieverWidget, self).__init__(parent)
            self.reactor = reactor
            self.setupLayout()
            self.connect()

        def setupLayout(self):
            #setup the layout and make all the widgets
            self.setWindowTitle('Reciever Widget')
            #create a horizontal layout
            layout = QtGui.QHBoxLayout()
            #create the text widget 
            self.textedit = QtGui.QTextEdit()
            self.textedit.setReadOnly(True)
            layout.addWidget(self.textedit)
            self.setLayout(layout)

        @inlineCallbacks
        def connect(self):
            #make an asynchronous connection to LabRAD
            from labrad.wrappers import connectAsync
            cxn = yield connectAsync(name = 'Signal Widget')
            self.server = cxn.emitter_server
            #connect to emitter server 
            yield self.server.signal__emitted_signal(self.ID)
            #connect to signal from server (note the method is named from parsed 
            #text of the in the server emitter name)
            yield self.server.addListener(listener = self.displaySignal, 
                    source = None, ID = self.ID) 
            #This registers the client as a listener to the server and assigns a 
            #slot (function) from the client to the signal emitted from the server
            #In this case self.displaySignal

        def displaySignal(self, cntx, signal):
            self.textedit.append(signal)

        def closeEvent(self, x):
            #stop the reactor when closing the widget
            self.reactor.stop()

    if __name__=="__main__":
        #join Qt and twisted event loops
        a = QtGui.QApplication( [] )
        import qt4reactor
        qt4reactor.install()
        from twisted.internet import reactor
        widget = recieverWidget(reactor)
        widget.show()
        reactor.run()
```
### Lets try it out

Run the server and make sure it is listed in your LabRAD manager as "Emitter Server". 

Run the client, the GUI text box should be displayed and blank.  The title of the window should be "Receiver Widget".  When the server emits a signal we expect the text box to show "Output!".

In order for the server to emit the signal we must call the function emitSignal() from the emitter server. Open a python terminal, import labrad and connect to the server
```python
    import labrad
    cxn = labrad.connect(name='python terminal')
    emitterserver = cxn.emitter_server
    emitterserver.emit_signal()
```
You should now see the text 'Output!' on your client GUI