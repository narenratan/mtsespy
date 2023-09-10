"""
Conveniences for handling MTS-ESP clients.
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
