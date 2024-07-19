"""
Set multi-channel tuning from scala files

Calling as

    $ python3 multi_channel.py example_1.scl example_1.kbm example_2.scl example_2.kbm

puts the tuning from example_1.scl on channel 0, example_2.scl on channel 1, and so on.
"""

import sys
import signal

import mtsespy as mts

with mts.Master():
    for channel, (scl_file, kbm_file) in enumerate(zip(sys.argv[1::2], sys.argv[2::2])):
        print(
            f"Setting tuning for midi channel {channel} from {scl_file} and {kbm_file}"
        )
        mts.set_multi_channel(True, channel)
        freqs = mts.scala_files_to_frequencies(scl_file, kbm_file)
        mts.set_multi_channel_note_tunings(freqs, channel)

    signal.pause()
