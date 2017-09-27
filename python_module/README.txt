jumany
======
Python interface for JUMAN Morphological analysis system.

`JUMAN <http://nlp.ist.i.kyoto-u.ac.jp/index.php?JUMAN>`

Requirement
-----------
- Windows 64bit system only
- Python 3.3 or above

Install
-------
```python setup.py install
```

How to use
----------
>>> import jumany
>>> jumany.open_lib()
True
>>> jumany.analyze("吾輩は猫である。")
[('吾輩', 'わがはい', '吾輩', 6, 1, 0, 0), ('は', 'は', 'は', 9, 2, 0, 0),('猫', 'ねこ', '猫', 6, 1, 0, 0), ('である', 'である', 'だ', 4, 0, 25, 15), ('。', ' 。', '。', 1, 1, 0, 0)]
>>> jumany.get_hinsi(6)
'名詞'
>>> jumany.get_bunrui(6,1)
'普通名詞'
>>> jumany.analyze("吾輩は猫である。\nまだ名前は無い。", True, True)
['吾輩', 'は', '猫', 'である', '。', 'まだ', '名前', 'は', '無い', '。']

See `jumany page <https://github.com/yujakudo/jumany/python_module>` for more details.

Licenses
--------
- Python scripts: BSD License
- Shared library for Windows: BSD License, but libraries under LGPL are linked.
