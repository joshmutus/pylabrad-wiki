### Introduction
pylabrad supports units: physical quantities with a unit such as meter or gigahertz.  It is required to use units when invoking labrad settings that specify units (type tag v[Hz] or similar), but it is recommended that you use them in all of your code to help avoid bugs like those that caused the crash of the [Mars Climate Orbiter](http://en.wikipedia.org/wiki/Mars_Climate_Orbiter).

### Examples

```python 
>>> import labrad.units as U
>>> from labrad.units import GHz, MHz, Hz, ms, us, ns, km, m, mm

>>> x = U.Value(10.0, 'm') # Construct the quantity 10 meters
>>> print x
10.0 m
>>> x.inUnitsOf('mm')  # Converts the units and returns a Value with the new units
Value(10000.0, 'mm')
>>> print x['mm'] # Extracts the floating point value 10000.0 -- x in millimeters
10000.0

>>> y = x / (2 * ns) # 5 meters / nanosecond
>>> y
Value(5.0, 'm/ns')
>>> print y['m/s']
4999999999.999999

>>> print 3*mm + 1*m 
1003.0 mm
```
Dimensioned quantities can be constructed either using the Value constructor (interchangeable with WithUnit or Complex), or by multiplying by the "unit" objects imported from labrad.units.  Basic arithmetic works as you expect: * and / multiply or divide units while + and - require the arguments to be in compatible units and do appropriate conversion.

Numpy ndarrays can also be given units (currently in the new_units development branch) in the same fashion.

```python
>>> import labrad.units as U
>>> m = U.Unit('m')

>>> x = np.array([1, 2, 3, 4, 5]) * m
>>> x['cm']
array([100, 200, 300, 400, 500])
>>> x[1:3]
ValueArray(array([2., 3.]), 'm') 
```

Any expression involving units which results in a dimensionless quantity (all of the base units cancel) generates an ordinary float/complex/ndarray which can be passed to any numeric function.  For instance `sin(2*np.pi*w*t)` will work properly if `w` and `t` have the appropriate units, but `sin(2*np.pi*t)` will not -- you cannot compute the sin of 3 seconds.  You can also get bare numbers out by using the x['ns'] notation.  Note that radians are a valid unit, but they don't get special treatment.  If you have quantities in radians you will need to use [] to extract a floating point.

```python
>>> x = 0.5*np.pi*rad
>>> np.sin(x) # raises an exception!
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: sin
>>> np.sin(x['rad'])
1.0
```

### Methods

In addition to the arithmetic operations, dimensioned quantities support the following methods and properties

**unit**<br>
    The quantity's units as a Unit object

**units**<br>
    A property that returns the quantity's units as a string

**inUnitsOf**(_unit_)<br>
    Convert the quantity to the specified unit and return an object with the new units.  This always returns the same type as the original (Value, Complex, ValueArray)

**inBaseUnits**(_unit_)<br>
    Convert to SI base units

**isCompatible**(_unit_)<br>
    Test to see if the value could be successfully converted to the specified units.

**isDimensionless**()<br>
    Test to see if the units cancel.  If this is true, you can treat the number just like a float/complex/array

**sqrt**()<br>
    Take the square root of the number including units

**__getitem__**(_unit_)<br>
The Indexing operator [] is used to convert to the specified units and then return that value as a base type (with no units attached).  For instance (5*MHz)['Hz'] == 1000000.0.
