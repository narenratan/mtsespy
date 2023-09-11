"""
Tests for mtsespy
"""
import pytest

import mtsespy as mts


def test_register_and_deregister_client():
    client = mts.register_client()
    mts.deregister_client(client)


def test_note_to_frequency():
    with mts.Client() as c:
        f = mts.note_to_frequency(c, 69, 0)
    assert f == 440.0


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
    assert mts.has_ipc() == True


def test_get_num_clients():
    with mts.Master():
        assert mts.get_num_clients() == 0
        with mts.Client():
            assert mts.get_num_clients() == 1
            with mts.Client():
                assert mts.get_num_clients() == 2
        assert mts.get_num_clients() == 0


def test_reinitialize():
    assert mts.can_register_master()
    mts.register_master()
    assert not mts.can_register_master()
    mts.reinitialize()
    assert mts.can_register_master()


def test_reinitialize_2():
    mts.register_master()
    mts.register_client()
    assert mts.get_num_clients() == 1
    mts.reinitialize()
    assert mts.get_num_clients() == 0
