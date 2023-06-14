import customtkinter
from encryption.passlocker import PasslockException
from .manager_view import Manager

banner = r"""
=*%@@%#=
:@@#-::-*@@:
:@@.       @@:
:@@+#@@@@%+@@:
|@@@@@/  \@@@@@|
#@@@@@\__/@@@@@#
:@@@@@@:.@@@@@@:
:%@@@@@@@@@@%:
:+#@@@@#+:
"""


class Login(customtkinter.CTkFrame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller

        self.banner = customtkinter.CTkLabel(
            master=self, text=banner, font=("Hack Regular", 12))
        self.banner.pack(pady=5, padx=25)

        self.label = customtkinter.CTkLabel(
            master=self, text="Passlock", font=("Hack Regular", 14))
        self.label.pack(pady=5, padx=25)

        self.passwd_field = customtkinter.CTkEntry(
            master=self,
            placeholder_text="Master Password",
            show="*",
            width=200)
        self.passwd_field.pack(pady=5, padx=25)

        self.passwd_field.bind("<Return>", self.on_enter_event)

        self.login_button = customtkinter.CTkButton(
            master=self,
            text="login",
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
            self.error_massage = customtkinter.CTkLabel(
                master=self,
                text=e.msg,
                text_color="red",
                font=("Hack Regular", 12))
            self.error_massage.pack()

    def on_enter_event(self, event):
        self.login()
