import customtkinter
from PIL import Image


class Generator(customtkinter.CTkFrame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(4, weight=1)

        # Menu Panel
        self.menu = GeneratorMenu(
            self,
            self.controller,
            border_color="grey",
            border_width=1
        )
        self.menu.grid(
            padx=(0, 5),
            row=0,
            column=0,
            columnspan=1,
            sticky="ns"
        )

        # MAIN PANEL
        self.generator_view = GeneratorView(
            self,
            self.controller,
            border_width=1,
            border_color="grey",
            label_text="Generators"

        )
        self.generator_view.grid(
            row=0,
            column=3,
            columnspan=3,
            sticky="nsew"
        )


class GeneratorMenu(customtkinter.CTkFrame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.parent = parent

        self.logo = customtkinter.CTkImage(Image.open('passlock_logo.png'), size=(157, 31))
        self.logo_label = customtkinter.CTkLabel(master=self, image=self.logo, text="")
        self.logo_label.pack(pady=12, padx=10)

        self.manager_button = customtkinter.CTkButton(
            master=self,
            text="Manager",
            command=self.switch_view
        )
        self.manager_button.pack(pady=15, padx=25, side="top")

        self.generator_button = customtkinter.CTkButton(
            master=self,
            text="Generators",
        )
        self.generator_button.pack(pady=15, padx=25, side="top")

        self.logout_button = customtkinter.CTkButton(
            master=self,
            text="Logout",
            command=self.logout
        )
        self.logout_button.pack(pady=15, padx=25, side="top")

     

    def logout(self):
        self.parent.destroy()
        from .login_view import Login
        self.controller.frames[Login] = Login(
            self.controller.container,
            self.controller
        )
        self.controller.show_frame(Login)

    def switch_view(self):
        self.parent.destroy()
        from .manager_view import Manager
        self.controller.frames[Manager] = Manager(
            self.controller.container,
            self.controller
        )
        self.controller.show_frame(Manager)


class GeneratorView(customtkinter.CTkScrollableFrame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Entry list
        self.password_generator_frame = PasswordGeneratorFrame(
            self,
            self.controller,
            border_width=1,
            border_color="grey"

        )

        self.passphrase_generator_frame = PassphraseGeneratorFrame(
            self,
            self.controller,
            border_width=1,
            border_color="grey"

        )

        self.token_generator_frame = TokenGeneratorFrame(
            self,
            self.controller,
            border_width=1,
            border_color="grey"
        )

        self.secretkey_generator_frame = SecrekeyGeneratorFrame(
            self,
            self.controller,
            border_width=1,
            border_color="grey"

        )

        self.password_generator_frame.pack(
            padx=10,
            pady=5,
            fill="x"
        )

        self.passphrase_generator_frame.pack(
            padx=10,
            pady=5,
            fill="x"
        )

        self.token_generator_frame.pack(
            padx=10,
            pady=5,
            fill="x"
        )

        self.secretkey_generator_frame.pack(
            padx=10,
            pady=5,
            fill="x"
        )


class PasswordGeneratorFrame(customtkinter.CTkFrame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.parent = parent
        self.font_size = 12
        self.password_length = 8

        self.title = customtkinter.CTkLabel(
            master=self,
            text="Password",
            font=("Hack Regular", 22)
        )
        self.title.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.value_label = customtkinter.CTkLabel(
            master=self,
            text=f"Length: {self.password_length}",
            font=("Hack Regular", self.font_size)
        )
        self.value_label.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        self.slider = customtkinter.CTkSlider(
            master=self,
            from_=8,
            to=64,
            command=self.set_password_length
        )
        self.slider.grid(row=1, column=0, pady=5, padx=(10, 0), sticky="w")

        self.output_field = customtkinter.CTkTextbox(
            master=self,
            height=30,
            width=300
        )
        self.output_field.grid(
            row=3, column=0, columnspan=2, pady=(5, 15), padx=10, sticky="w")

        self.gen_button = customtkinter.CTkButton(
            master=self,
            text="Generate",
            command=self.gen_password
        )
        self.gen_button.grid(row=3, column=4,
                             pady=(5, 15), padx=10)

    def set_password_length(self, value):
        self.password_length = round(value)
        self.value_label.configure(text=f"Length: {self.password_length}")

    def gen_password(self):
        password = self.controller.interface.gen_password(self.password_length)
        self.update_ouput(password)

    def update_ouput(self, text):
        self.output_field.delete("0.0", "end")
        self.output_field.insert("0.0", f"{text}")


class PassphraseGeneratorFrame(customtkinter.CTkFrame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.parent = parent
        self.font_size = 12
        self.password_length = 4

        self.title = customtkinter.CTkLabel(
            master=self,
            text="Passphrase",
            font=("Hack Regular", 22)
        )
        self.title.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.value_label = customtkinter.CTkLabel(
            master=self,
            text=f"Length: {self.password_length}",
            font=("Hack Regular", self.font_size)
        )
        self.value_label.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        self.check_var = customtkinter.BooleanVar(value=False)
        self.checkbox = customtkinter.CTkCheckBox(
            master=self,
            text="Add Complexity",
            variable=self.check_var,
            onvalue=True,
            offvalue=False
        )
        self.checkbox.grid(row=1, column=2, pady=5, padx=10, sticky="w")

        self.slider = customtkinter.CTkSlider(
            master=self,
            from_=4,
            to=32,
            command=self.set_password_length
        )
        self.slider.grid(row=1, column=0, pady=5, padx=(10, 0), sticky="w")

        self.output_field = customtkinter.CTkTextbox(
            master=self,
            height=30,
            width=300
        )
        self.output_field.grid(
            row=3, column=0, columnspan=2, pady=(5, 15), padx=10, sticky="w")

        self.gen_button = customtkinter.CTkButton(
            master=self,
            text="Generate",
            command=self.gen_password
        )
        self.gen_button.grid(row=3, column=2,
                             pady=(5, 15), padx=10)

    def set_password_length(self, value):
        self.password_length = round(value)
        self.value_label.configure(text=f"Length: {self.password_length}")

    def gen_password(self):
        password = self.controller.interface.gen_passphrase(
            self.password_length, self.check_var.get()
        )
        self.update_ouput(password)

    def update_ouput(self, text):
        self.output_field.delete("0.0", "end")
        self.output_field.insert("0.0", f"{text}")


class TokenGeneratorFrame(customtkinter.CTkFrame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.parent = parent
        self.font_size = 12
        self.password_length = 8

        self.title = customtkinter.CTkLabel(
            master=self,
            text="Token",
            font=("Hack Regular", 22)
        )
        self.title.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.value_label = customtkinter.CTkLabel(
            master=self,
            text=f"Length: {self.password_length}",
            font=("Hack Regular", self.font_size)
        )
        self.value_label.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        self.slider = customtkinter.CTkSlider(
            master=self,
            from_=8,
            to=128,
            command=self.set_password_length
        )
        self.slider.grid(row=1, column=0, pady=5, padx=(10, 0), sticky="w")

        self.output_field = customtkinter.CTkTextbox(
            master=self,
            height=30,
            width=300
        )
        self.output_field.grid(
            row=3, column=0, columnspan=2, pady=(5, 15), padx=10, sticky="w")

        self.gen_button = customtkinter.CTkButton(
            master=self,
            text="Generate",
            command=self.gen_password
        )
        self.gen_button.grid(row=3, column=4,
                             pady=(5, 15), padx=10)

    def set_password_length(self, value):
        self.password_length = round(value)
        self.value_label.configure(text=f"Length: {self.password_length}")

    def gen_password(self):
        password = self.controller.interface.gen_token(
            self.password_length)
        self.update_ouput(password)

    def update_ouput(self, text):
        self.output_field.delete("0.0", "end")
        self.output_field.insert("0.0", f"{text}")


class SecrekeyGeneratorFrame(customtkinter.CTkFrame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.parent = parent
        self.font_size = 12
        self.password_length = 8

        self.title = customtkinter.CTkLabel(
            master=self,
            text="Secretkey",
            font=("Hack Regular", 22)
        )
        self.title.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.value_label = customtkinter.CTkLabel(
            master=self,
            text=f"Length: {self.password_length}",
            font=("Hack Regular", self.font_size)
        )
        self.value_label.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        self.slider = customtkinter.CTkSlider(
            master=self,
            from_=12,
            to=512,
            command=self.set_password_length
        )
        self.slider.grid(row=1, column=0, pady=5, padx=(10, 0), sticky="w")

        self.output_field = customtkinter.CTkTextbox(
            master=self,
            height=30,
            width=300
        )
        self.output_field.grid(
            row=3, column=0, columnspan=2, pady=(5, 15), padx=10, sticky="w")

        self.gen_button = customtkinter.CTkButton(
            master=self,
            text="Generate",
            command=self.gen_password
        )
        self.gen_button.grid(row=3, column=4,
                             pady=(5, 15), padx=10)

    def set_password_length(self, value):
        self.password_length = round(value)
        self.value_label.configure(text=f"Length: {self.password_length}")

    def gen_password(self):
        password = self.controller.interface.gen_secretkey(
            self.password_length)
        self.update_ouput(password)

    def update_ouput(self, text):
        self.output_field.delete("0.0", "end")
        self.output_field.insert("0.0", f"{text}")
