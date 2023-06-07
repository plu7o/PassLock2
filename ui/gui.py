import customtkinter
from .interface import Interface

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


class Gui(customtkinter.CTk):
    def __init__(self, interface: Interface):
        super().__init__()
        self.interface = interface

        container = customtkinter.CTkFrame(master=self)
        container.pack(
            pady=10, padx=10,
            side="bottom",
            fill="both",
            expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Login, Manager):
            frame = F(container, self)
            self.frames[F] = frame
        self.show_frame(Manager)

    def show_frame(self, container):
        frame = self.frames[container]
        if isinstance(frame, Login):
            frame.grid(row=0, column=0, sticky="")
        else:
            frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()


class Login(customtkinter.CTkFrame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller

        self.label = customtkinter.CTkLabel(
            master=self, text='Login', font=("Hack Regular", 24))
        self.label.pack(pady=15, padx=25)

        self.passwd_field = customtkinter.CTkEntry(
            master=self,
            placeholder_text="Password",
            show="*",
            width=200)
        self.passwd_field.pack(pady=15, padx=25)

        self.login_button = customtkinter.CTkButton(
            master=self,
            text="login",
            command=self.login,
            width=200)
        self.login_button.pack(pady=15, padx=25)


################# UPDATE TO USE INTERFACE INSTEAD ########################

    def login(self):
        try:
            self.passlocker = Passlocker(self.passwd_field.get())
            self.destroy()
            self.controller.show_frame(Manager)
        except PasslockException as e:
            print(f"debug: {e.msg}")
            self.error_massage = customtkinter.CTkLabel(
                master=self,
                text=e.msg,
                text_color="red",
                font=("Hack Regular", 12))
            self.error_massage.pack()


class Manager(customtkinter.CTkFrame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(4, weight=1)

        # Menu Panel
        self.menu = ManagerMenu(
            self,
            self.controller,
            border_color="grey",
            border_width=1
        )
        self.menu.grid(
            padx=5,
            row=0,
            column=0,
            columnspan=1,
            sticky="ns"
        )
        # MAIN PANEL
        self.password_view = Password_view(
            self,
            self.controller,
            border_width=1,
            border_color="grey"
        )
        self.password_view.grid(
            padx=10,
            row=0,
            column=3,
            columnspan=3,
            sticky="nsew"
        )


class Password_view(customtkinter.CTkFrame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Searchbar
        self.searchbar = Searchbar(
            self,
            self.controller,
            fg_color="black"
        )
        self.searchbar.pack(
            padx=10,
            pady=10,
            fill="x"
        )

        # Entry list
        self.entry_list = EntryList(
            self,
            self.controller,
            fg_color="black"
        )
        self.entry_list.pack(
            padx=10,
            pady=10,
            ipadx=10,
            ipady=10,
            fill="both",
            expand=True
        )


class EntryList(customtkinter.CTkScrollableFrame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller
        for _ in range(5):
            item_frame = EntryItem(
                self,
                self.controller,
                border_width=1,
                border_color="white",
                height=50,
            )
            item_frame.pack(fill="x", ipadx=10, padx=5, pady=3)


class Separator(customtkinter.CTkLabel):
    def __init__(self, parent, font_size, **kwargs):
        super().__init__(
            parent,
            text='|',
            font=("Hack Regular", font_size),
            **kwargs)

        self.pack(pady=10, padx=10, side="left")


class EntryItem(customtkinter.CTkFrame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.font_size = 12

        self.username = customtkinter.CTkLabel(
            master=self,
            text='username',
            font=("Hack Regular", self.font_size)
        )
        self.username.pack(pady=5, padx=5, side="left")

        Separator(self, self.font_size)

        self.website = customtkinter.CTkLabel(
            master=self,
            text='https://website.com',
            font=("Hack Regular", self.font_size)
        )
        self.website.pack(pady=5, padx=5, side="left")

        Separator(self, self.font_size)

        self.note = customtkinter.CTkLabel(
            master=self,
            text='"Lorem ipsum blablabla"',
            font=("Hack Regular", self.font_size)
        )
        self.note.pack(pady=5, padx=5, side="left")

        Separator(self, self.font_size)

        self.password = customtkinter.CTkLabel(
            master=self,
            text='pass**************',
            font=("Hack Regular", self.font_size)
        )
        self.password.pack(pady=5, padx=5, side="left")

        Separator(self, self.font_size)

        self.show_button = customtkinter.CTkButton(
            master=self,
            text="👁",
            width=15
        )
        self.show_button.pack(pady=5, padx=5, side="right")


class Searchbar(customtkinter.CTkFrame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.search_field = customtkinter.CTkEntry(
            master=self,
            placeholder_text="search",
        )
        self.search_field.pack(
            pady=10, padx=10, fill="x", expand=True, side="left")

        self.search_button = customtkinter.CTkButton(
            master=self,
            text="Search"
        )
        self.search_button.pack(pady=10, padx=10, side="left", fill="x")


class ManagerMenu(customtkinter.CTkFrame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller

        self.label = customtkinter.CTkLabel(
            master=self,
            text='Passlock',
            font=("Hack Regular", 24)
        )
        self.label.pack(pady=12, padx=10)

        self.manager_button = customtkinter.CTkButton(
            master=self,
            text="Manager"
        )
        self.manager_button.pack(pady=15, padx=25, side="top")

        self.generator_button = customtkinter.CTkButton(
            master=self,
            text="Generators"
        )
        self.generator_button.pack(pady=15, padx=25, side="top")

        self.logout_button = customtkinter.CTkButton(
            master=self,
            text="Logout"
        )
        self.logout_button.pack(pady=15, padx=25, side="top")

    def logout(self):
        self.destroy()
        self.controller.show_frame(Login)
