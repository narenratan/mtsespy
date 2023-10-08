"""
Launchpad X tuning script

Tune a scale and set key colors for the Novation Launchpad X midi controller.

For details of setting up the Launchpad using midi see the Launchpad X
Programmer's Reference Guide available here:

    https://downloads.novationmusic.com/novation/launchpad-mk3/launchpad-x

Direct link to pdf:

    https://fael-downloads-prod.focusrite.com/customer/prod/s3fs-public/downloads/Launchpad%20X%20-%20Programmers%20Reference%20Manual.pdf

Requires the Python packages mido and python-rtmidi as well as mtsespy.
"""
import signal
from itertools import product

import mido

import mtsespy as mts

# Midi note map for Launchpad
# Maps x, y coordinates of each key (x keys across and y keys up from the
# bottom left key) to midi note number sent by Launchpad in programmer mode.
# See page 10 of Launchpad Programmer Reference Guide.

MIDI_NOTE_MAP = {(i, j): 10 * j + i + 11 for i, j in product(range(8), repeat=2)}


def map_scale(scale_length, steps):
    """
    Map scale degrees onto Launchpad keys.

    Parameters
    ----------
    scale_length : int
        Number of notes in scale to be mapped.

    steps : tuple of (int, int)
        The number of scale degrees to move when going in the x (across) and y
        (up) directions on the Launchpad. For example to go one scale degree up
        going along a row and five scale degrees up when going up a column, pass
        (1, 5).

    Returns
    -------
    dict of {(int, int) : (int, int)}
        Mapping from key coordinates to pairs of octave number and scale
        degree. Tells you which scale degree in which octave each Launchpad key
        is mapped to.
    """
    x, y = steps

    tuning_map = {}

    for (i, j), n in MIDI_NOTE_MAP.items():
        octave, degree = divmod(i * x + j * y, scale_length)
        tuning_map[i, j] = (octave, degree)

    return tuning_map


def tune(scale, tuning_map, base_freq=261.625565):
    """
    Tune synth to play scale on Launchpad.

    Waits for interrupt after tuning is applied (can kill script with Ctrl-C
    or pkill for example).

    Parameters
    ----------
    scale : list of float or Fraction
        List of frequency ratios in scale to be tuned. Elements can be for
        example 5/4 for just intonation or 2**(10/31) for an equal temperament.
    tuning_map : dict of {(int, int) : (int, int)}
        Map from Launchpad key coordinates to octave and scale degree pairs,
        as returned by `map_scale`.
    base_freq : optional float
        Frequency in Hz to assign to 1.0 frequency ratio. Defaults to middle
        C frequency.
    """
    with mts.Master():
        for (i, j), n in MIDI_NOTE_MAP.items():
            octave, degree = tuning_map[i, j]
            mts.set_note_tuning(2**octave * scale[degree] * base_freq, n)
        signal.pause()


def set_key_colors(tuning_map, color_map, launchpad_port):
    """
    Set key colors on Launchpad.

    Colors are set via midi - see Launchpad Programmer Reference pages 12-14.

    Parameters
    ----------
    tuning_map : dict of {(int, int) : (int, int)}
        Map from Launchpad key coordinates to octave and scale degree pairs,
        as returned by `map_scale`.
    color_map : dict of {int : int}
        Map from scale degrees to Launchpad color numbers. See Programmer
        Reference page 12 for the 128 available colors.
    launchpad_port : mido.ports.BaseOutput
        Midi output port for Launchpad. As returned by `mido.open_output`.
    """
    for (i, j), (octave, degree) in tuning_map.items():
        if degree in color_map:
            launchpad_port.send(
                mido.Message(
                    "note_on", note=MIDI_NOTE_MAP[i, j], velocity=color_map[degree]
                )
            )


def init_launchpad():
    """
    Initial setup of Launchpad.

    Returns
    -------
    mido.ports.BaseOutput
        Midi port for sending messages to Launchpad.
    """
    # Connect to Launchpad midi
    launchpad_output_names = [x for x in mido.get_output_names() if "LPX MIDI In" in x]
    if not launchpad_output_names:
        raise RuntimeError("Could not find Launchpad Midi input")
    output_name = launchpad_output_names[0]
    outport = mido.open_output(output_name)

    # Switch Launchpad to programmer mode
    header = [0x00, 0x20, 0x29, 0x02, 0x0C]
    outport.send(mido.Message("sysex", data=header + [14, 1]))

    # Turn off all key LEDs
    for i in MIDI_NOTE_MAP.values():
        outport.send(mido.Message("note_off", note=i))

    return outport


def main():
    """
    Tune scale and set Launchpad key colors.
    """

    # Set scale here
    # Example below is 19EDO
    scale = [2 ** (i / 19) for i in range(19)]

    # Set number of scale degrees to move going across and up on the Launchpad here
    # Example below is 1 scale degree moving across, 5 scale degrees moving up.
    steps = 1, 5

    outport = init_launchpad()

    tuning_map = map_scale(len(scale), steps)

    # Set color for each scale degree here
    # See Launchpad Programmer Reference page 12 for the 128 available colors.
    color_map = {0: 3, 8: 41, 11: 45}

    set_key_colors(tuning_map, color_map, outport)

    outport.close()

    tune(scale, tuning_map)


if __name__ == "__main__":
    main()
