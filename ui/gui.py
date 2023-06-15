import customtkinter
from .interface import Interface
from .views.login_view import Login

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


class Gui(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.interface = Interface()
        self.logged_in = False
        self.geometry("1280x620")
        self.title("Passlock")

        self.container = customtkinter.CTkFrame(master=self)
        self.container.pack(
            pady=10, padx=10,
            side="bottom",
            fill="both",
            expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        frame = Login(self.container, self)
        self.frames[Login] = frame
        self.show_frame(Login)

    def show_frame(self, container):
        frame = self.frames[container]
        if isinstance(frame, Login):
            frame.grid(row=0, column=0, sticky="", ipady=10)
        else:
            frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def exit(self):
        self.destroy()
