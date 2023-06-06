from models.enrty import Entry
from encryption.passlocker import Passlocker
from storage.storage import StorageManager
from ui.cli import Cli
from ui.gui import Gui

def main():
    # passlocker = Passlocker('hallo')
    gui = Gui()
    gui.mainloop()


if __name__ == '__main__':
    main()
