jumany
======
Python interface for JUMAN Morphological analysis system.

`JUMAN <http://nlp.ist.i.kyoto-u.ac.jp/index.php?JUMAN>`

Requirement
-----------
- POSIX system, Windows 64bit system
- Python 3.3 or above

Installation
------------
```python setup.py install
```

How to use
----------
>>> import jumany
>>> jumany.open_lib()
True
>>> jumany.analyze("<your Japanese text>")

See `jumany page <https://github.com/yujakudo/jumany/python_module>` for more details in Japanese.

Licenses
--------
- Python scripts: BSD License
- Pre-built libraries for Windows: BSD License, but libraries under LGPL are linked.
