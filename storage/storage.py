import csv
import os

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
            writer.writerow([entry.service,
                             entry.username,
                             entry.url,
                             entry.note,
                             entry.email,
                             self.passlocker.encrypt(entry.password)])

    def delete_entry(self, index: int):
        rows = self.get_all_rows()
        if 0 <= index < len(rows):
            del rows[index]
            self.write_all_rows(rows)

    def update_entry(self, index: int, entry):
        rows = self.get_all_rows()
        if 0 <= index < len(rows):
            rows[index] = [entry.service,
                           entry.username,
                           entry.url,
                           entry.note,
                           entry.email,
                           self.passlocker.encrypt(entry.password)]
            self.write_all_rows(rows)

    def write_all_rows(self, rows):
        with open(self.storage_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

    def get_all_rows(self):
        rows = []
        with open(self.storage_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                rows.append(row)
        return rows

    def get_all(self):
        rows = []
        with open(self.storage_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                rows.append(Entry(*row))
        return rows

    def new(self):
        with open(self.storage_file, 'a', newline='') as file:
            pass

    def search(self, value, column_index=0):
        found_rows = []
        with open(self.storage_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if column_index < len(row) and row[column_index] == value:
                    found_rows.append(row)
        return found_rows
