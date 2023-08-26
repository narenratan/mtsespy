"""
Set multi-channel tuning from csv
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
