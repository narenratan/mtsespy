"""
Tests for mtsespy
"""
import pytest

import mtsespy as mts
from mtsespy import scala_files_to_frequencies


@pytest.fixture(autouse=True)
def reinit():
    mts.reinitialize()


def test_register_and_deregister_client():
    client = mts.register_client()
    mts.deregister_client(client)


def test_register_and_deregister_master():
    mts.register_master()
    mts.deregister_master()


def test_can_register_master():
    assert mts.can_register_master()


def test_note_to_frequency():
    with mts.Client() as c:
        f = mts.note_to_frequency(c, 69, 0)
    assert f == 440.0


def test_retuning_in_semitones():
    with mts.Client() as c:
        semitones = mts.retuning_in_semitones(c, 69, 0)
    assert semitones == 0.0


def test_retuning_in_semitones_2():
    with mts.Master():
        mts.set_note_tuning(440 * 2 ** (1 / 24), 69)
        with mts.Client() as c:
            semitones = mts.retuning_in_semitones(c, 69, 0)
    assert abs(semitones - 0.5) <= 1e-6


def test_retuning_as_ratio():
    with mts.Client() as c:
        ratio = mts.retuning_as_ratio(c, 69, 0)
    assert ratio == 1.0


def test_retuning_as_ratio_2():
    retune_ratio = 25 / 24
    with mts.Master():
        mts.set_note_tuning(440 * retune_ratio, 69)
        with mts.Client() as c:
            ratio = mts.retuning_as_ratio(c, 69, 0)
    assert abs(ratio - retune_ratio) < 1e-6


def test_master_context_manager():
    """
    Test that client pulls master's new frequency if used within Master context.
    """
    with mts.Master():
        mts.set_note_tuning(441.0, 69)
        with mts.Client() as c:
            f = mts.note_to_frequency(c, 69, 0)
    assert f == 441.0


def test_master_context_manager_2():
    """
    Test that client pulls default frequency if used outside Master context.
    """
    with mts.Master():
        mts.set_note_tuning(441.0, 69)
    with mts.Client() as c:
        f = mts.note_to_frequency(c, 69, 0)
    assert f == 440.0


def test_master_exists_error():
    with pytest.raises(mts.MasterExistsError):
        with mts.Master():
            with mts.Master():
                pass


def test_set_note_tunings():
    frequencies = list(range(128))
    with mts.Master():
        mts.set_note_tunings(frequencies)
        with mts.Client() as c:
            client_frequencies = [mts.note_to_frequency(c, i, 0) for i in range(128)]
    assert frequencies == client_frequencies


def test_has_ipc():
    assert mts.has_ipc()


def test_get_num_clients():
    assert mts.get_num_clients() == 0
    with mts.Client():
        assert mts.get_num_clients() == 1
        with mts.Client():
            assert mts.get_num_clients() == 2
        assert mts.get_num_clients() == 1
    assert mts.get_num_clients() == 0


def test_reinitialize():
    assert mts.can_register_master()
    mts.register_master()
    assert not mts.can_register_master()
    mts.reinitialize()
    assert mts.can_register_master()


def test_reinitialize_2():
    mts.register_client()
    assert mts.get_num_clients() == 1
    mts.reinitialize()
    assert mts.get_num_clients() == 0


def test_get_scale_name():
    with mts.Client() as c:
        name = mts.get_scale_name(c)
    assert name == "12-TET"


def test_set_scale_name():
    with mts.Master():
        mts.set_scale_name("foo")
        with mts.Client() as c:
            name = mts.get_scale_name(c)
    assert name == "foo"


def test_should_filter_note():
    with mts.Client() as c:
        should_filter = mts.should_filter_note(c, 69, 0)
    assert not should_filter


def test_filter_note():
    with mts.Master():
        mts.filter_note(True, 69, 0)
        with mts.Client() as c:
            should_filter = mts.should_filter_note(c, 69, 0)
    assert should_filter


def test_clear_note_filter():
    with mts.Master():
        mts.filter_note(True, 69, 0)
        mts.clear_note_filter()
        with mts.Client() as c:
            should_filter = mts.should_filter_note(c, 69, 0)
    assert not should_filter


def test_set_multi_channel_note_tuning():
    with mts.Master():
        mts.set_multi_channel(True, 0)
        mts.set_multi_channel_note_tuning(441.0, 69, 0)
        with mts.Client() as c:
            f = mts.note_to_frequency(c, 69, 0)
    assert f == 441.0


def test_set_multi_channel_note_tuning_2():
    with mts.Master():
        mts.set_multi_channel(False, 0)
        mts.set_multi_channel_note_tuning(441.0, 69, 0)
        with mts.Client() as c:
            f = mts.note_to_frequency(c, 69, 0)
    assert f == 440.0


def test_set_multi_channel_note_tunings():
    frequencies = list(range(128))
    with mts.Master():
        mts.set_multi_channel(True, 0)
        mts.set_multi_channel_note_tunings(frequencies, 0)
        with mts.Client() as c:
            client_frequencies = [mts.note_to_frequency(c, i, 0) for i in range(128)]
    assert frequencies == client_frequencies


def test_set_multi_channel_note_tunings_2():
    frequencies = list(range(128))
    with mts.Master():
        mts.set_multi_channel(False, 0)
        mts.set_multi_channel_note_tunings(frequencies, 0)
        with mts.Client() as c:
            client_frequencies = [mts.note_to_frequency(c, i, 0) for i in range(128)]
    assert frequencies != client_frequencies


def test_filter_note_multi_channel():
    with mts.Master():
        mts.set_multi_channel(True, 1)
        mts.filter_note_multi_channel(True, 69, 1)
        with mts.Client() as c:
            should_filter = mts.should_filter_note(c, 69, 1)
    assert should_filter


def test_clear_note_filter_multi_channel():
    with mts.Master():
        mts.set_multi_channel(True, 1)
        mts.filter_note_multi_channel(True, 69, 1)
        mts.clear_note_filter_multi_channel(1)
        with mts.Client() as c:
            should_filter = mts.should_filter_note(c, 69, 1)
    assert not should_filter


def test_clear_note_filter_multi_channel_2():
    with mts.Master():
        mts.set_multi_channel(True, 1)
        mts.filter_note_multi_channel(True, 69, 1)
        mts.clear_note_filter_multi_channel(0)
        with mts.Client() as c:
            should_filter = mts.should_filter_note(c, 69, 1)
    assert should_filter


def test_has_master():
    with mts.Master():
        with mts.Client() as c:
            does_have_master = mts.has_master(c)
    assert does_have_master


def test_has_master_2():
    with mts.Client() as c:
        does_have_master = mts.has_master(c)
    assert not does_have_master


def test_frequency_to_note():
    with mts.Client() as c:
        note = mts.frequency_to_note(c, 441.0, 0)
    assert note == 69


def test_frequency_to_note_2():
    with mts.Master():
        mts.set_note_tuning(441.0, 80)
        with mts.Client() as c:
            note = mts.frequency_to_note(c, 441.0, 0)
    assert note == 80


def test_frequency_to_note_and_channel():
    with mts.Client() as c:
        note, channel = mts.frequency_to_note_and_channel(c, 441.0)
    assert note == 69
    assert channel == 0


def test_frequency_to_note_and_channel_2():
    with mts.Master():
        mts.set_note_tuning(441.0, 80)
        with mts.Client() as c:
            note, channel = mts.frequency_to_note_and_channel(c, 441.0)
    assert note == 80
    assert channel == 0


def test_frequency_to_note_and_channel_3():
    with mts.Master():
        mts.set_multi_channel(True, 1)
        mts.set_multi_channel_note_tuning(441.0, 80, 1)
        with mts.Client() as c:
            note, channel = mts.frequency_to_note_and_channel(c, 441.0)
    assert note == 80
    assert channel == 1


def test_parse_midi_data():
    # MTS sysex message to tune midi note 69 up a quarter tone
    msg = bytes.fromhex("F0 7F 00 08 02 00 01" + "45" + "45 40 00" + "F7")
    with mts.Client() as c:
        f_before = mts.note_to_frequency(c, 69, 0)
        mts.parse_midi_data(c, msg)
        f_after = mts.note_to_frequency(c, 69, 0)
    assert f_before == 440.0
    assert abs(f_after - 440.0 * 2 ** (1 / 24)) < 1e-3


def test_scala_files_to_frequencies(tmp_path):
    scl_path = tmp_path / "test.scl"
    kbm_path = tmp_path / "test.kbm"

    scl_path.write_text(
        """Test scl
 12
!
 16/15
 9/8
 6/5
 5/4
 4/3
 7/5
 3/2
 8/5
 5/3
 9/5
 15/8
 2/1
"""
    )

    kbm_path.write_text(
        """12
  0
  127
  60
  69
  440.0
  12
!
  0
  1
  2
  3
  4
  5
  6
  7
  8
  9
  10
  11
"""
    )

    frequencies = scala_files_to_frequencies(str(scl_path), str(kbm_path))
    assert abs(frequencies[69] - 440.0) <= 1e-8
    assert abs(frequencies[61] / frequencies[60] - 16 / 15) <= 1e-8
