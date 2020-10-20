# UnitTest Resolver

Execute all unittests that refers to a specific function in python. Build as an extension to Contour.


```sh
usage: cli.py [-h] --module MODULE --target TARGET
```



## Example
Consider the following basic case:
```py

import unittest

def increment(num: int) -> int:
    return num+=1
    
class Test(unittest.TestCase):
    def testMisc(self):
        self.assertEqual(increment(6), 7)
        
    def test(self):
        self.assertEqual(increment(4), 4)

    def randomTest(self):
        doLongWork()
```

UnitTest Resolver will run the unittest class functions (`testMisc`, `test`) that refer to the target function.

Resolver **may** fail if the test class functions are stateful.


## Limitations
The primary limitation is that binding is limited to the single module level. Future work may address this, so that parsing and execution can happen at any level.

Another limitation is that currenty we're restricted to one context in execution. Future work can address this as well.

