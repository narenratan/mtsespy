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
