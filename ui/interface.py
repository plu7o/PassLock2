from models.enrty import Entry
from storage.storage import StorageManager
from encryption.passlocker import Passlocker
from encryption.generators import PasswordGenerator, PassphraseGenerator, TokenGenerator, SecretkeyGenerator


class Interface():
    def __init__(self):
        pass

    def login(self, password):
        self.passlocker = Passlocker(password)
        self.storage = StorageManager(self.passlocker)

    def logout(self):
        pass

    def add_entry(self, service, username, url, email, password):
        new_entry = Entry(service, username, url, email, password)
        self.storage.save_entry(new_entry)

    def del_entry(self, id):
        self.storage.delete_entry(id)

    def update_entry(self, id, service, username, url, email, password):
        entry = Entry(service, username, url, email, password)
        self.storage.update_entry(id, entry)

    def search_entry(self, query) -> list[Entry]:
        return self.storage.search(query)

    def get_all_entries(self) -> list[Entry]:
        return self.storage.get_all()

    def gen_password(self, length):
        return PasswordGenerator.gen_password(length)

    def gen_passphrase(self, length, complexity):
        return PassphraseGenerator.gen_passphrase(length, complexity)

    def gen_token(self, length):
        return TokenGenerator.gen_token(length)

    def gen_secretkey(self, length):
        return SecretkeyGenerator.gen_secret_key(length)
