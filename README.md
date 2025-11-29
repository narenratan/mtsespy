# mtsespy
Python bindings for the [ODDSound MTS-ESP library](https://oddsound.com/devs.php).

## Installation

To install from PyPI:
```console
$ pip install mtsespy
```
or to clone the repo and install from source:
```console
$ git clone --recurse-submodules https://github.com/narenratan/mtsespy.git
$ cd mtsespy
$ python3 -m pip install .
```

Using MTS-ESP requires the libMTS dynamic library which is available in the
ODDSound MTS-ESP repo
[here](https://github.com/ODDSound/MTS-ESP/tree/main/libMTS/). The places to
put it for each OS are given in the MTS-ESP README
[here](https://github.com/oddsound/mts-esp?tab=readme-ov-file#libmts). To use
MTS-ESP on ARM, for example on a Raspberry Pi, you can build the open source
libMTS in [this repo](https://github.com/baconpaul/mts-dylib-reference).

## Examples

Set tuning of midi note 69 to frequency 441 Hz
```python
import signal

import mtsespy as mts

with mts.Master():
    mts.set_note_tuning(441.0, 69)
    signal.pause()
```

Pull frequency of midi note 69 on midi channel 0
```python
import mtsespy as mts

with mts.Client() as c:
    f = mts.note_to_frequency(c, 69, 0)
```

The `Master` and `Client` context managers, used above, handle registering
and deregistering the MTS-ESP master and client.

## Wrapper names

The function names in the MTS-ESP C++ library and this Python wrapper
correspond as follows

### Master functions

|   C++                             |   Python                          |
| --------------------------------- | --------------------------------- |
|   MTS_RegisterMaster              |   register_master                 |
|   MTS_DeregisterMaster            |   deregister_master               |
|   MTS_HasIPC                      |   has_ipc                         |
|   MTS_Reinitialize                |   reinitialize                    |
|   MTS_Master_ShouldUpdateLibrary  |   master_should_update_library    |
|   MTS_GetNumClients               |   get_num_clients                 |
|   MTS_SetNoteTunings              |   set_note_tunings                |
|   MTS_SetNoteTuning               |   set_note_tuning                 |
|   MTS_SetScaleName                |   set_scale_name                  |
|   MTS_SetPeriodRatio              |   set_period_ratio                |
|   MTS_SetMapSize                  |   set_map_size                    |
|   MTS_SetMapStartKey              |   set_map_start_key               |
|   MTS_SetRefKey                   |   set_ref_key                     |
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
|   MTS_Client_ShouldUpdateLibrary  |   client_should_update_library    |
|   MTS_ShouldFilterNote            |   should_filter_note              |
|   MTS_NoteToFrequency             |   note_to_frequency               |
|   MTS_RetuningInSemitones         |   retuning_in_semitones           |
|   MTS_RetuningAsRatio             |   retuning_as_ratio               |
|   MTS_FrequencyToNote             |   frequency_to_note               |
|   MTS_FrequencyToNoteAndChannel   |   frequency_to_note_and_channel   |
|   MTS_GetScaleName                |   get_scale_name                  |
|   MTS_GetPeriodRatio              |   get_period_ratio                |
|   MTS_GetPeriodSemitones          |   get_period_semitones            |
|   MTS_GetMapSize                  |   get_map_size                    |
|   MTS_GetMapStartKey              |   get_map_start_key               |
|   MTS_GetRefKey                   |   get_ref_key                     |
|   MTS_ParseMIDIDataU              |   -                               |
|   MTS_ParseMIDIData               |   parse_midi_data                 |
|   MTS_HasReceivedMTSSysEx         |   has_received_mts_sysex          |


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
or, using a default keyboard mapping,
```python
frequencies = scala_files_to_frequencies("tuning.scl")
```
and returns a list of 128 frequencies in Hz, one for each each midi note.
