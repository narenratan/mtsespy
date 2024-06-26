"""
Context managers for MTS-ESP clients and master
"""

import signal
import sys
from pathlib import Path

import mtsespy as mts


def _check_dso():
    """
    Check the MTS-ESP dynamic shared object is installed and has IPC.
    """
    dso_path = {
        "linux": Path("/usr/local/lib/libMTS.so"),
        "darwin": Path("/Library/Application Support/MTS-ESP/libMTS.dylib"),
        "win32": Path("/Program Files/Common Files/MTS-ESP/LIBMTS.dll"),
    }[sys.platform]
    if not dso_path.exists():
        msg = f"MTS-ESP dynamic shared object '{dso_path}' not found.\n\n{dso_path.name} can be downloaded from https://github.com/ODDSound/MTS-ESP/tree/main/libMTS"
        raise FileNotFoundError(msg)
    if not mts.has_ipc():
        msg = f"IPC not available for MTS-ESP.\n\nEither '{dso_path}' does not support IPC or IPC is disabled in MTS-ESP.conf"
        raise RuntimeError(msg)


def _deregister_master_handler(signum, frame):
    print(f"Deregistering master after receiving {signal.Signals(signum).name}")
    mts.deregister_master()
    sys.exit(128 + signum)


class Client:
    """
    Context manager to automatically register and deregister client.
    """

    def __init__(self):
        _check_dso()
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
        _check_dso()
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
