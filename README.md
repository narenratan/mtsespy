# Python bindings for ODDSound MTS-ESP

## Installation

Currently only Linux is supported. To build and install:
```console
$ git clone https://github.com/narenratan/mtsespy.git
$ cd mtsespy
$ git submodule update --init --recursive
$ python3 -m pip install .
```

## Examples

Set tuning of midi note 69 to frequency 441 Hz
```python
import mtsespy as mts

with mts.Master():
    mts.set_note_tuning(441.0, 69)
```

Pull frequency of midi note 69 on midi channel 0
```python
import mtsespy as mts

with mts.Client() as c:
    f = mts.note_to_frequency(c, 69, 0)
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


## Scala files

The `mtsespy` package also includes a `scala_files_to_frequencies`
function which uses the Surge Synth Team [Tuning Library](https://github.com/surge-synthesizer/tuning-library).
This is not part of the MTS-ESP library; it's included because I find
it convenient to be able to use tunings in Scala scl and kbm files with
MTS-ESP in Python.  The `scala_files_to_frequencies` function can be
called as
```python
from mtsespy import scala_files_to_frequencies

frequencies = scala_files_to_frequencies("tuning.scl", "tuning.kbm")
```
and returns a list of 128 frequencies in Hz, one for each each midi note.
