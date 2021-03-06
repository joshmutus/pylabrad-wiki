LabRAD servers advertise type tags for each argument in their settings. These type tags specify what types of data are allowed to be passed to the setting. On the sending side, the pylabrad client must take a given python object and convert it to one of the types advertised by the recipient setting.

Here we specify how various combinations of python objects and type tags should be handled by pylabrad. Python objects are written assuming the following imports

```python
from labrad.units import Hz, mHz
from labrad.units import WithUnit
```

| LabRAD type tag | Python data      | Value sent by pylabrad | Type tag sent by pylabrad |
| :--------------:|:-----------------|:-----------------------|:--------------------------|
| b               | b = True/False   | b                      | 'b' |
| b               | x = non-boolean  | bool(x)                | 'b' |
| i               | 3                | 3                      | 'i' |
| i               | -4               | -4                     | 'i' |
| i               | 4.4              | error                  | - |
| w               | 234              | 234                    | 'w' |
| w               | -234             | error                  | - |
| w               | 2**40            | error                  | - |
| 'v[Hz]'         | 4.5*Hz           | 4.5 Hz                 | 'v[Hz]' |
| 'v[Hz]'         | 4.5*mHz          | 0.0045 Hz              | 'v[Hz]' |
| 'v[Hz]'         | 4.5*s            | error                  | - |
| 'v[Hz]'         | 4.5              | error                  | - |
| 'v[]'           | 4.5              | 4.5                    | 'v[]' |
| 'v[]'           | 4.5*Hz           | error                  | - |
| 'v[]'           | 4                | float(4)               | 'v[]' |
| 'v'             | 4.5              | 4.5                    | 'v[]' |
| 'v'             | 4.5*Hz           | 4.5 Hz                 | 'v[Hz]' |
| '?'             | x = True/False   | x                      | 'b' |
| '?'             | 5                | 5                      | 'i' |
| '?'             | -5               | -5                     | 'i' |
| '?'             | 5L               | 5                      | 'w' |
| '?'             | -5L              | error / 5 (??)         | -/'i'   |
| '?'             | 5.0              | 5.0                    | v[] |
| '?'             | WithUnit(5, '')  | 5.0                    | v[] |
| '?'             | 5.0*Hz           | 5.0                    | v[Hz] |
| '*v'            | [3*Hz, 5*km]     | error                  | - |
| '*v'            | [3*Hz, 5*kHz]    | [3.0, 5000.0]          | v[Hz] |
| '*v[kHz]'       |  [3*Hz, 5*kHz]     | [.003, 5.0]       | v[kHz] |
| '*i'            | array(x,np.int32)  | x                 | *i |
| '*i'            | array(x,np.int64)  | x (*)             | *i |
| '*i'            | array(x,np.uintNN) | x (*)             | *i |
| '*w'            | array(x,np.intNN)  | x (*)             | *w |
| '*w'            | array(x,np.uintNN) | x (*)             | *w |
| '*?'            | array(x,np.intNN)  | x (*)             | *i |
| '*?'            | array(x,np.uintNN) | x (*)             | *w |

(*) Numpy integer type (int32,int64,uint32,uint64) conversions to 'i'/'w' may be subject to bounds checking.