# Python bindings for ODDSound MTS-ESP

Currently work in progress. If you'd like to build and use this:
```console
$ git clone https://github.com/narenratan/mtsespy.git
$ cd mtsespy
$ git submodule update --init --recursive
$ python3 -m pip install .
```

Example master interpreter session:
```python
>>> import mtsespy as mts
>>> mts.register_master()
>>> mts.set_note_tuning(81/80 * 8.175798915643707, 0)
```

Example client interpreter session:
```python
>>> import mtsespy as mts
>>> client = mts.register_client()
>>> mts.note_to_frequency(client, 0, 0)
8.175798915643707
>>> mts.retuning_in_semitones(client, 0, 0)
0.0
>>> mts.retuning_as_ratio(client, 0, 0)
1.0
>>> mts.note_to_frequency(client, 0, 0)
8.277996063232422
>>> mts.retuning_in_semitones(client, 0, 0)
0.21506218729265011
>>> mts.retuning_as_ratio(client, 0, 0)
1.0124999585536736
```
