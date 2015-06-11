To add modules:
----------------------
* Filename lowercase with '\_' as spaces. Classes using full caps as MyClassName. Methods, functions and variables also follow lowercase with '\_' convention (PEP8).
* Make a new python file under the relevant header (detection, reconstruction etc.) and add the name to the \_\_init\_\_.py as following "from .FILENAME import CLASSNAME". This makes the class visible in the cogradio package.
* Write tests under the relevant category (sampling_tests, reconstruction_tests, etc.). For information on the test suite read about the nose package for Python. The tests can be run with the command 'nosetests' from the top directory (where this file is located).
