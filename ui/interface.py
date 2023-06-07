from encryption.paslocker import Passlocker, PasslockException
from storage.storage import StorageManager


class Interface():
    def __init__(self):
        self.passlocker = Passloker()
        self.storage = StorageManager(self.passlocker)
