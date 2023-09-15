"""
Context managers for MTS-ESP clients and master
"""
import signal
import sys

import mtsespy as mts


def _deregister_master_handler(signum, frame):
    print(f"Deregistering master after receiving {signal.Signals(signum).name}")
    mts.deregister_master()
    sys.exit(128 + signum)


class Client:
    """
    Context manager to automatically register and deregister client.
    """

    def __init__(self):
        self._client = mts.register_client()

    def __enter__(self):
        return self._client

    def __exit__(self, exc_type, exc_val, exc_tb):
        mts.deregister_client(self._client)


class Master:
    """
    Context manager to automatically register and deregister master.

    If a master already exists then `MasterExistsError` is raised.
    """

    def __init__(self):
        if not mts.can_register_master():
            raise MasterExistsError("An MTS-ESP master is already registered")
        self._handler = signal.getsignal(signal.SIGTERM)
        signal.signal(signal.SIGTERM, _deregister_master_handler)
        mts.register_master()

    def __enter__(self):
        return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        signal.signal(signal.SIGTERM, self._handler)
        mts.deregister_master()


class MasterExistsError(Exception):
    pass
