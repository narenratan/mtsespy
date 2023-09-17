# Python bindings for ODDSound MTS-ESP

# Installation
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

### Master functions

|   C++                             |   Python                          |
| --------------------------------- | --------------------------------- |
|   MTS_RegisterMaster              |   register_master                 |
|   MTS_DeregisterMaster            |   deregister_master               |
|   MTS_HasIPC                      |   has_ipc                         |
|   MTS_Reinitialize                |   reinitialize                    |
|   MTS_GetNumClients               |   get_num_clients                 |
|   MTS_SetNoteTunings              |   set_note_tunings                |
|   MTS_SetNoteTuning               |   set_note_tuning                 |
|   MTS_SetScaleName                |   set_scale_name                  |
|   MTS_FilterNote                  |   filter_note                     |
|   MTS_ClearNoteFilter             |   clear_note_filter               |
|   MTS_SetMultiChannel             |   set_multi_channel               |
|   MTS_SetMultiChannelNoteTunings  |   set_multi_channel_note_tunings  |
|   MTS_SetMultiChannelNoteTuning   |   set_multi_channel_note_tuning   |
|   MTS_FilterNoteMultiChannel      |   filter_note_multi_channel       |
|   MTS_ClearNoteFilterMultiChannel |   clear_note_filter_multi_channel |

### Client functions

|   C++                             |   Python                          |
| --------------------------------- | --------------------------------- |
|   MTS_RegisterClient              |   register_client                 |
|   MTS_DeregisterClient            |   deregister_client               |
|   MTS_HasMaster                   |   has_master                      |
|   MTS_ShouldFilterNote            |   should_filter_note              |
|   MTS_NoteToFrequency             |   note_to_frequency               |
|   MTS_RetuningInSemitones         |   retuning_in_semitones           |
|   MTS_RetuningAsRatio             |   retuning_as_ratio               |
|   MTS_FrequencyToNote             |   frequency_to_note               |
|   MTS_FrequencyToNoteAndChannel   |   frequency_to_note_and_channel   |
|   MTS_GetScaleName                |   get_scale_name                  |
|   MTS_ParseMIDIDataU              |   -                               |
|   MTS_ParseMIDIData               |   parse_midi_data                 |
