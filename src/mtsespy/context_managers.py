"""
Context managers for MTS-ESP clients and master
"""
import mtsespy as mts


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
        mts.register_master()

    def __enter__(self):
        return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        mts.deregister_master()


class MasterExistsError(Exception):
    pass
