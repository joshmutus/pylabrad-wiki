LabRAD data is specified by type tags that specify the binary format and interpretation of data transmitted over the network.  pylabrad maps these data types to native python types, so data received from the network is automatically unflattened to the appropriate python type, and vice versa.  

| LabRAD type tag | Python data type | Notes |
| ---------------:|-----------------:|------:|
| b               | True/False       | Boolean value |
| i               | int              | 32 bit signed integer |
| w               | long             | 32 bit unsigned integer |
| v[unit]         | Value(x, 'unit') | Real number with physical units |
| v[]             | float            | Dimensionless real / floating point value |
| c[unit]         | Complex(a+1j*b, 'unit') | Complex number with physical units |
| c[]             | complex          | Dimensionless complex number |
| v, c            |                  | float/complex with unspecified units.  Deprecated, use v[] and c[] |
| *X              | list/ndarray     | list(*) of elements of type 'X' |
| *nX             | list/ndarray     | n-dimensional list(*)/array of type 'X' |
| (...)           | tuple            | cluster of elements with specified type |
| t               | datetime.datetime | Time stamp |
| E, E?           | Exception        | Error message with optional payload(**) |
| _               | None             | Null type |
| ?               | n/a              | Any labrad data(**) | 

(*) LabRAD list types unflatten as a LazyList -- a type that emulates a list but doesn't unflatten the raw data until you use it.  If it is passed on to another labrad server, it need never be unflattened.  In addition, if the list holds numeric data, the .asarray property unflattens it as a numpy ndarray which is much more efficient for large data structures.

(**) ? is an incomplete data type.  LabRAD servers can advertise ? to indicate they accept or return any type of labrad data, but it is always replaced with a concrete data type when transmitted over the wire.