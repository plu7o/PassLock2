import csv
import os
import stat
import difflib
import platform
from pathlib import Path
from models.enrty import Entry


class StorageManager():
    def __init__(self, passlocker) -> None:
        self.passlocker = passlocker
        if platform.system() == "Linux":
            storage_folder = Path.home() / ".passlock"
            if not storage_folder.exists():
                storage_folder.mkdir(0o600)
            self.storage_file = storage_folder / "entries.csv"
        
        elif platform.system() == "Windows":
            storage_folder = Path.home() / r"AppData\Local\passlock"
            if not storage_folder.exists():
                storage_folder.mkdir(mode=0o600)
                os.system(f'attrib +h "{storage_folder}"')
            self.storage_file = storage_folder / "entries.csv"

        if not os.path.exists(self.storage_file):
            self.new()

    def save_entry(self, entry):
        with open(self.storage_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                self.passlocker.encrypt(entry.service).decode(),
                self.passlocker.encrypt(entry.username).decode(),
                self.passlocker.encrypt(entry.url).decode(),
                self.passlocker.encrypt(entry.email).decode(),
                self.passlocker.encrypt(entry.password).decode()
            ])

    def delete_entry(self, index: int):
        rows = self.get_all_rows()
        if 0 <= index < len(rows):
            del rows[index]
            self.write_all_rows(rows)

    def update_entry(self, index: int, entry):
        rows = self.get_all_rows()
        if 0 <= index < len(rows):
            rows[index] = [
                self.passlocker.encrypt(entry.service).decode(),
                self.passlocker.encrypt(entry.username).decode(),
                self.passlocker.encrypt(entry.url).decode(),
                self.passlocker.encrypt(entry.email).decode(),
                self.passlocker.encrypt(entry.password).decode()
            ]
            self.write_all_rows(rows)

    def write_all_rows(self, rows):
        with open(self.storage_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

    def get_all_rows(self) -> list[list[str]]:
        rows = []
        with open(self.storage_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                rows.append(row)
        return rows

    def get_all(self) -> list[Entry]:
        rows = []
        for _id, row in enumerate(self.get_all_rows()):
            decrypted = [self.passlocker.decrypt(
                value.encode()) for value in row]
            rows.append(
                Entry(
                    *decrypted,
                    _id
                )
            )
        return rows

    def new(self):
        # creates a new empty file
        with open(self.storage_file, 'a', newline=''):
            pass
        os.chmod(self.storage_file, stat.S_IRUSR | stat.S_IWUSR)

    def search(self, query, threshold=0.5) -> list[Entry]:
        match_items = []
        for item in self.get_all():
            service = difflib.SequenceMatcher(
                None, query, item.service).ratio()
            username = difflib.SequenceMatcher(
                None, query, item.username).ratio()
            url = difflib.SequenceMatcher(
                None, query, item.url).ratio()
            email = difflib.SequenceMatcher(
                None, query, item.email).ratio()

            hits = [True if hit >= threshold else False for hit in [
                service, username, url, email]]

            if any(hits):
                match_items.append(item)

        return match_items
