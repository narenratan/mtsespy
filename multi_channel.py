"""
Set multi-channel tuning from csv
"""
import csv

import mtsespy as mts

mts.register_master()

with open("tuning.csv", newline="") as f:
    reader = csv.reader(f)
    rows = list(reader)[1:]

for i in range(16):
    mts.set_multi_channel(True, i)

for frequency, note, channel in rows:
    mts.set_multi_channel_note_tuning(float(frequency), int(note), int(channel))
