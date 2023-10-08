import signal
from itertools import product

import mido

import mtsespy as mts

# MIDI note map for Launchpad programmer mode

MIDI_NOTE_MAP = {(i, j): 10 * j + i + 11 for i, j in product(range(8), repeat=2)}


def map_scale(scale, steps):
    x, y = steps

    tuning_map = {}

    for (i, j), n in MIDI_NOTE_MAP.items():
        octave, degree = divmod(i * x + j * y, len(scale))
        tuning_map[i, j] = (octave, degree)

    return tuning_map


def tune(scale, tuning_map, base_freq=261.625565):
    with mts.Master():
        for (i, j), n in MIDI_NOTE_MAP.items():
            octave, degree = tuning_map[i, j]
            mts.set_note_tuning(2**octave * scale[degree] * base_freq, n)
        signal.pause()


def set_key_colors(tuning_map, color_map, launchpad_port):
    # Map from scale degrees to Launchpad key color midi note

    for (i, j), (octave, degree) in tuning_map.items():
        if degree in color_map:
            launchpad_port.send(
                mido.Message(
                    "note_on", note=MIDI_NOTE_MAP[i, j], velocity=color_map[degree]
                )
            )


def init_launchpad():
    # Connect to launchpad midi
    launchpad_output_names = [x for x in mido.get_output_names() if "LPX MIDI In" in x]
    if not launchpad_output_names:
        raise RuntimeError("Could not find Launchpad Midi input")
    output_name = launchpad_output_names[0]
    outport = mido.open_output(output_name)

    # Switch launchpad to programmer mode
    header = [0x00, 0x20, 0x29, 0x02, 0x0C]
    outport.send(mido.Message("sysex", data=header + [14, 1]))

    # Turn off LEDs
    for i in MIDI_NOTE_MAP.values():
        outport.send(mido.Message("note_off", note=i))

    return outport


def main():
    scale = [2 ** (i / 19) for i in range(19)]

    steps = 1, 5

    outport = init_launchpad()

    tuning_map = map_scale(scale, steps)

    color_map = {0: 3, 8: 41, 11: 45}

    set_key_colors(tuning_map, color_map, outport)

    outport.close()

    tune(scale, tuning_map)


if __name__ == "__main__":
    main()
