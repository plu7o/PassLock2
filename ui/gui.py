import customtkinter
from encryption.passlocker import PasslockException, Passlocker


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


class Gui(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        container = customtkinter.CTkFrame(master=self)
        container.pack(pady=10, padx=10,
                       side="bottom",
                       fill="both",
                       expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Login, Manager):
            frame = F(container, self)
            self.frames[F] = frame

        self.show_frame(Login)

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

        self.side_panel = customtkinter.CTkFrame(master=self)
        self.side_panel.grid(row=0, column=0, columnspan=1, sticky="ns")

        self.label = customtkinter.CTkLabel(
            master=self.side_panel, text='Passlock', font=("Hack Regular", 24))
        self.label.pack(pady=12, padx=10)

        self.manager_button = customtkinter.CTkButton(
            master=self.side_panel,
            text="Manager",
            width=200)
        self.manager_button.pack(pady=15, padx=25)

        self.generator_button = customtkinter.CTkButton(
            master=self.side_panel,
            text="Generators",
            width=200)
        self.generator_button.pack(pady=15, padx=25)

        self.main_panel = customtkinter.CTkFrame(master=self)
        self.main_panel.grid(row=0, column=1, columnspan=3, sticky="nsew")

        self.label = customtkinter.CTkLabel(
            master=self.main_panel, text='right', font=("Hack Regular", 24))
        self.label.pack(pady=12, padx=10)

        self.grid(row=0, column=1, sticky="")

    def logout(self):
        self.destroy()
        self.controller.show_frame(Login)
