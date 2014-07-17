pylabrad supports units: physical quantities with a unit such as meter or gigahertz.  It is required to use units when invoking labrad settings that specify that they take a quantity with specific units (type tag v[Hz] or similar), but it is recommended that you use them in all of your code to help avoid bugs like those that crashed the Mars Climate Orbiter.

```python 
import labrad.units as U
from labrad.units import GHz, MHz, Hz, ms, us, ns, km, m, mm

x = WithUnit(10.0, 'm') # Construct the quantity 10 meters
y = x / (2 * ns) # 5 meter / nanosecond
x['mm'] # Returns the value 10000.0 -- x represented in nanoseconds
```
