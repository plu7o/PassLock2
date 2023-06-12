import csv
import os
import difflib
from models.enrty import Entry


class StorageManager():
    def __init__(self, passlocker) -> None:
        self.passlocker = passlocker
        self.storage_file = "entries.csv"
        if not os.path.exists(self.storage_file):
            self.new()

    def save_entry(self, entry):
        with open(self.storage_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                entry.service,
                entry.username,
                entry.url,
                entry.email,
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
                entry.service,
                entry.username,
                entry.url,
                entry.email,
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
            rows.append(
                Entry(
                    *row[:-1],
                    self.passlocker.decrypt(row[-1].encode()),
                    _id
                )
            )
        return rows

    def new(self):
        # creates a new empty file
        with open(self.storage_file, 'a', newline=''):
            pass

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

            print(service, username, url, email)

            hits = [True if hit >= threshold else False for hit in [
                service, username, url, email]]

            if any(hits):
                match_items.append(item)

        return match_items
