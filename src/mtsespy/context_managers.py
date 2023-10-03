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

    If a master already exists then `MasterExistsError` is raised.  Signal
    handlers are added to call `deregister_master` on SIGINT or SIGTERM.
    """

    def __init__(self):
        if not mts.can_register_master():
            raise MasterExistsError("An MTS-ESP master is already registered")
        # Store existing signal handlers
        self._handlers = {
            x: signal.getsignal(x) for x in [signal.SIGINT, signal.SIGTERM]
        }
        for x in self._handlers:
            signal.signal(x, _deregister_master_handler)
        mts.register_master()

    def __enter__(self):
        return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restore original signal handlers
        for k, v in self._handlers.items():
            signal.signal(k, v)
        mts.deregister_master()


class MasterExistsError(Exception):
    pass
