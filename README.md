# Python bindings for ODDSound MTS-ESP

To build and install:
```console
$ git clone https://github.com/narenratan/mtsespy.git
$ cd mtsespy
$ git submodule update --init --recursive
$ python3 -m pip install .
```

## Examples
Set tuning of one midi note
```python
>>> with mts.Master():
...     mts.set_note_tuning(441.0, 69)
```

Pull frequency of a midi note
```python
>>> with mts.Client() as c:
...     f = mts.note_to_frequency(c, 69, 0)
...
>>> f
440.0
```

## Wrapper names
All functions in the MTS-ESP library are wrapped. The function names
correspond as follows

|   C++                     |   Python              |
| ------------------------- | --------------------- |
|   MTS_RegisterMaster      |   register_master     |
|   MTS_DeregisterMaster    |   deregister_master   |
