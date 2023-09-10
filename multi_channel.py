"""
Set multi-channel tuning from scala files

Calling as

    $ python3 -i multi_channel_from_scala.py example.scl example.kbm example_2.scl example_2.kbm

puts the tuning from example.scl on channel 0, example_2.scl on channel 1, and so on.
"""
import sys

import mtsespy as mts

mts.register_master()

for i in range(16):
    mts.set_multi_channel(True, i)

for channel, (scl_file, kbm_file) in enumerate(zip(sys.argv[1::2], sys.argv[2::2])):
    freqs = mts.scala_files_to_frequencies(scl_file, kbm_file)
    for note, f in enumerate(freqs):
        mts.set_multi_channel_note_tuning(f, note, channel)
