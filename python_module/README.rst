======
jumany
======
Python interface for
`JUMAN Morphological analysis system <http://nlp.ist.i.kyoto-u.ac.jp/index.php?JUMAN>`_ .

Requirement
-----------
- POSIX or Windows
- Python 3.3 or above

Installation
------------
::

    pip install jumany

How to use
----------
::

    import jumany
    jumany.open_lib()
    jumany.analyze("吾輩は猫である。")

See `jumany page <https://github.com/yujakudo/jumany>`_ for more details in Japanese.

License
--------
- Python scripts: BSD License
- Library: BSD License
- Pre-built library for Windows: BSD License, additionally libraries under LGPL are linked.
