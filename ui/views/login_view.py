import customtkinter
import time
from encryption.passlocker import PasslockException
from .manager_view import Manager
from PIL import Image


banner = r"""
_::++::_
=*%@@%#=
:@@#-::-*@@:
:@@.       @@:
:@+#@@@@%+@:
|@@@@/  \@@@@|
#@@@@\__/@@@@#
:@@@@@:.@@@@@:
:%@@@@@@@@%:
:+#@@@@#+:
"""



mesg_dict = {
    1: "Na Vaddi wirst alt? Passwort vergessen!",
    2: "Komm schon du pimmel, versuch's nochmal!",
    3: "Letze Chance sonst wirds nervig!!!",
}


class Login(customtkinter.CTkFrame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.trys = 0
        self.sleep_time = 1
        self.controller = controller
        self.error_massage = None

        self.banner = customtkinter.CTkLabel(
            master=self, text=banner, anchor="nw" , font=("Hack Regular", 12))
        self.banner.pack(pady=5, padx=25)

        self.logo = customtkinter.CTkImage(Image.open('passlock_logo.png'), size=(157, 31))
        self.logo_label = customtkinter.CTkLabel(master=self, image=self.logo, text="")
        self.logo_label.pack(pady=12, padx=10)

        self.passwd_field = customtkinter.CTkEntry(
            master=self,
            placeholder_text="Master Password",
            show="*",
            justify="center",
            width=200)
        self.passwd_field.pack(pady=5, padx=25)

        self.passwd_field.bind("<Return>", self.on_enter_event)

        self.login_button = customtkinter.CTkButton(
            master=self,
            text="Authenticate",
            command=self.login,
            width=200)
        self.login_button.pack(pady=5, padx=25)

    def login(self):
        try:
            self.controller.interface.login(self.passwd_field.get())
            self.controller.logged_in = True

            self.destroy()
            self.controller.frames[Manager] = Manager(
                self.controller.container,
                self.controller
            )
            self.controller.show_frame(Manager)
        except PasslockException as e:
            self.trys += 1
            if self.trys <= 3:
                if self.error_massage is not None:
                    self.error_massage.destroy()
                self.error_massage = customtkinter.CTkLabel(
                    master=self,
                    text=f"{e.msg}\n{mesg_dict.get(self.trys)}",
                    font=("Hack Regular", 12))
                self.error_massage.pack(pady=5, padx=5)
            else:
                self.error_massage.destroy()
                self.error_massage = customtkinter.CTkLabel(
                    master=self,
                    text=f"{e.msg}\n If you are a Hacker Fuck You🖕\n sleeping {self.sleep_time} sec...💤",
                    text_color="red",
                    font=("Hack Regular", 12))
                self.error_massage.pack(pady=5, padx=5)
                time.sleep(self.sleep_time)
                self.sleep_time *= 2

    def on_enter_event(self, event):
        self.login()
