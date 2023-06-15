import customtkinter
from PIL import Image


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
            padx=(0, 5),
            row=0,
            column=0,
            columnspan=1,
            sticky="ns"
        )
        # MAIN PANEL
        self.password_view = PasswordView(
            self,
            self.controller,
            border_width=1,
            border_color="grey"
        )
        self.password_view.grid(
            row=0,
            column=3,
            columnspan=3,
            sticky="nsew"
        )


class ManagerMenu(customtkinter.CTkFrame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.parent = parent

        self.logo = customtkinter.CTkImage(Image.open('passlock_logo.png'), size=(157, 31))
        self.logo_label = customtkinter.CTkLabel(master=self, image=self.logo, text="")
        self.logo_label.pack(pady=12, padx=10)

        self.manager_button = customtkinter.CTkButton(
            master=self,
            text="Manager"
        )
        self.manager_button.pack(pady=15, padx=25, side="top")

        self.generator_button = customtkinter.CTkButton(
            master=self,
            text="Generators",
            command=self.switch_view
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
        from .generator_view import Generator
        self.controller.frames[Generator] = Generator(
            self.controller.container,
            self.controller
        )
        self.controller.show_frame(Generator)


class PasswordView(customtkinter.CTkFrame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Entry list
        self.entry_list = EntryList(
            self,
            self.controller,
            orientation="vertical",
            label_text="ID | SERVICE | USERNAME | URL | EMAIL | PASSWORD",
            label_anchor="center",
        )
        # Searchbar
        self.searchbar = Searchbar(
            self.entry_list,
            self,
            self.controller,
            # fg_color="black"
        )

        self.option_menu = OptionsMenu(
            self.entry_list,
            self,
            self.controller,
            height=70,
        )

        self.searchbar.pack(
            padx=(10, 5),
            pady=10,
            fill="x"
        )

        self.option_menu.pack(
            padx=10,
            pady=5,
            fill="x"
        )

        self.entry_list.pack(
            padx=10,
            pady=(5, 10),
            ipadx=5,
            ipady=5,
            fill="both",
            expand=True
        )


class OptionsMenu(customtkinter.CTkFrame):
    def __init__(self, entry_list, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.entry_list = entry_list
        self.toplevel_window = None

        self.add_button = customtkinter.CTkButton(
            master=self,
            text="Add +",
            width=15,
            command=self.add_entry
        )
        self.add_button.pack(pady=5, padx=5, fill="x",
                             expand=True, side="left")

    def add_entry(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            # create window if its None or destroyed
            self.toplevel_window = AddDialog(
                self.entry_list, self, self.controller)
            self.toplevel_window.focus()
        else:
            self.toplevel_window.focus()


class AddDialog(customtkinter.CTkToplevel):
    def __init__(self, entry_lsit, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.entry_list = entry_lsit
        self.controller = controller
        self.parent = parent
        self.toplevel_window = None
        self.geometry("400x300")
        self.width = 120
        self.passwd = self.controller.interface.gen_password(12)
        self.title("Add Entry")

        self.frame = customtkinter.CTkFrame(self)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame.grid(ipadx=10, ipady=10, row=0, column=0, sticky="")

        self.service = customtkinter.CTkEntry(
            self.frame,
            placeholder_text="Service",
            width=self.width
        )
        self.service.pack(pady=(10, 5), padx=5, fill="x", side="top")
        self.username = customtkinter.CTkEntry(
            self.frame,
            placeholder_text="Username",
            width=self.width
        )
        self.username.pack(pady=5, padx=5, fill="x", side="top")
        self.url = customtkinter.CTkEntry(
            self.frame,
            placeholder_text="url",
            width=self.width
        )
        self.url.pack(pady=5, padx=5, fill="x", side="top")

        self.email = customtkinter.CTkEntry(
            self.frame,
            placeholder_text="Email",
            width=self.width
        )
        self.email.pack(pady=5, padx=5, fill="x", side="top")

        self.password_menu_var = customtkinter.StringVar(value="Generate Password")
        self.password_menu = customtkinter.CTkOptionMenu(
            master=self.frame,
            values=["Generate Password", "Generate Passphrase", "Manual Password"],
            command=self.optionmenu_callback,
            variable=self.password_menu_var
        )
        self.password_menu.pack(pady=5, padx=5, fill="x", side="top")

        self.password = customtkinter.CTkEntry(
                master=self.frame,
                placeholder_text="Password",
                width=self.width
            )

        self.confirm_button = customtkinter.CTkButton(
            master=self.frame,
            text="Confirm",
            width=150,
            command=self.add_entry,
        )
        self.confirm_button.pack(pady=5, padx=5, fill="x", side="left")
        self.cancel_button = customtkinter.CTkButton(
            master=self.frame,
            text="Cancel",
            width=150,
            command=self.destroy,
        )
        self.cancel_button.pack(pady=5, padx=5, fill="x", side="right")
    
    def optionmenu_callback(self, choice):
        if choice == "Generate Password":
            if self.password.winfo_exists():
                self.password.destroy()
            self.passwd = self.controller.interface.gen_password(12)
        if choice == "Generate Passphrase":
            if self.password.winfo_exists():
                self.password.destroy()
            self.passwd = self.controller.interface.gen_passphrase(4, False)
        if choice == "Manual Password":
            self.confirm_button.destroy()
            self.cancel_button.destroy()
            self.password = customtkinter.CTkEntry(
                master=self.frame,
                placeholder_text="Password",
                width=self.width
            )
            self.password.pack(pady=5, padx=5, fill="x", side="top")
            self.confirm_button = customtkinter.CTkButton(
                master=self.frame,
                text="Confirm",
                width=150,
                command=self.add_entry,
            )
            self.confirm_button.pack(pady=5, padx=5, fill="x", side="left")
            self.cancel_button = customtkinter.CTkButton(
                master=self.frame,
                text="Cancel",
                width=150,
                command=self.destroy,
            )
            self.cancel_button.pack(pady=5, padx=5, fill="x", side="right")
            self.passwd = None

    def add_entry(self):
        service = self.service.get()
        username = self.username.get()
        url = self.url.get()
        email = self.email.get()
        password = self.passwd if self.passwd is not None else self.password.get()
        fields = [True if field == "" else False for field in [
            service, username, url, email, password]]

        # check if any filed is empty
        if any(fields):
            self.error()
            return

        self.controller.interface.add_entry(
            service, username, url, email, password)
        self.destroy()
        self.update_results()

    def error(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            # create window if its None or destroyed
            self.toplevel_window = ErrorDialog(
                self, self.controller
            )
            self.toplevel_window.focus()

        else:
            self.toplevel_window.focus()

    def update_results(self):
        self.clear_results()
        results = self.controller.interface.get_all_entries()

        for _, result in enumerate(results):
            create_entry(
                result,
                self.entry_list,
                self.controller
            )

    def clear_results(self):
        for widget in self.entry_list.winfo_children():
            if isinstance(widget, EntryItem):
                widget.destroy()


class ErrorDialog(customtkinter.CTkToplevel):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.width = 130
        self.geometry("400x300")
        self.title("Error")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.msg_frame = customtkinter.CTkFrame(self)
        self.msg_frame.grid(ipadx=10, ipady=10, row=0, column=0, sticky="")

        self.msg = customtkinter.CTkLabel(
            master=self.msg_frame,
            text="Du hast was vergessen du pimmel!\n alles ausfüllen.",
            width=self.width
        )
        self.msg.pack(padx=10, pady=10, fill="x")
        self.confirm_button = customtkinter.CTkButton(
            master=self.msg_frame,
            text="Ok",
            width=150,
            command=self.confirm
        )
        self.confirm_button.pack(pady=5, padx=(10, 5), fill="x")

    def confirm(self):
        self.destroy()


class EntryList(customtkinter.CTkScrollableFrame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller
        for entry in self.controller.interface.get_all_entries():
            create_entry(
                entry,
                self,
                self.controller,
            )


class EntryItem(customtkinter.CTkFrame):
    def __init__(self, entry, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.font_size = 12
        self.entry = entry
        self.entry_list = parent
        self.toplevel_window = None

     

        self.service = customtkinter.CTkTextbox(
            master=self,
            font=("Hack Regular", self.font_size),
            width=len(self.entry.service),
            height=10,
        )
        self.service.insert("0.0", self.entry.service)
        self.service.configure(state="disabled")
        self.service.pack(pady=5, padx=(5, 2.5), side="left", fill="x", expand=True)
        self.service.bind("<Double-Button-1>", self.double_click)
        #Separator(self, self.font_size)

        self.username = customtkinter.CTkTextbox(
            master=self,
            font=("Hack Regular", self.font_size),
            width=len(self.entry.username),
            height=10
        )
        self.username.insert("0.0", self.entry.username)
        self.username.configure(state="disabled")
        self.username.pack(pady=5, padx=2.5, side="left", fill="x", expand=True)
        self.username.bind("<Double-Button-1>", self.double_click)
        #Separator(self, self.font_size)

        self.website = customtkinter.CTkTextbox(
            master=self,
            font=("Hack Regular", self.font_size),
            width=len(self.entry.url),
            height=10
        )
        self.website.insert("0.0", self.entry.url)
        self.website.configure(state="disabled")
        self.website.pack(pady=5, padx=2.5, side="left", fill="x", expand=True)
        self.website.bind("<Double-Button-1>", self.double_click)
       # Separator(self, self.font_size)

        self.email = customtkinter.CTkTextbox(
            master=self,
            font=("Hack Regular", self.font_size),
            width=len(self.entry.email),
            height=10
        )
        self.email.insert("0.0", self.entry.email)
        self.email.configure(state="disabled")
        self.email.pack(pady=5, padx=2.5, side="left", fill="x", expand=True)
        self.email.bind("<Double-Button-1>", self.double_click)
        #Separator(self, self.font_size)

        self.password = customtkinter.CTkTextbox(
            master=self,
            font=("Hack Regular", self.font_size),
            width=len(self.entry.password),
            height=10
        )
        self.password.insert("0.0", self.entry.password)
        self.password.configure(state="disabled")
        self.password.pack(pady=5, padx=2.5, side="left", fill="x", expand=True)
        self.password.bind("<Double-Button-1>", self.double_click)
        #Separator(self, self.font_size)

        self.del_button = customtkinter.CTkButton(
            master=self,
            text="✗",
            width=20,
            command=self.delete
        )
        self.del_button.pack(pady=5, padx=(0, 15), side="right")

        self.update_button = customtkinter.CTkButton(
            master=self,
            text="✏",
            width=20,
            command=self.update
        )
        self.update_button.pack(pady=5, padx=5, side="right")

    def double_click(self, event):
        # text = event.widget["text"]
        text = event.widget.get("0.0", "end")
        self.copy_text(text)

    def copy_text(self, text):
        self.controller.clipboard_clear()
        self.controller.clipboard_append(text)

    def delete(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            # create window if its None or destroyed
            self.toplevel_window = ConfirmDialog(
                self.entry.id, self.entry_list, self, self.controller)
            self.toplevel_window.focus()

        else:
            self.toplevel_window.focus()

    def update(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            # create window if its None or destroyed
            self.toplevel_window = UpdateDialog(
                self.entry, self.entry_list, self, self.controller)
            self.toplevel_window.focus()

        else:
            self.toplevel_window.focus()


class UpdateDialog(customtkinter.CTkToplevel):
    def __init__(self, entry, entry_lsit, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.entry_list = entry_lsit
        self.controller = controller
        self.entry = entry
        self.geometry("400x300")
        self.width = 120
        self.title(f"Update Entry: {self.entry.id}")

        self.frame = customtkinter.CTkFrame(self)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame.grid(ipadx=10, ipady=10, row=0, column=0, sticky="")

        self.service = customtkinter.CTkEntry(
            self.frame,
            placeholder_text=self.entry.service,
            width=self.width
        )
        self.service.pack(pady=(10, 5), padx=5, fill="x")
        self.username = customtkinter.CTkEntry(
            self.frame,
            placeholder_text=self.entry.username,
            width=self.width
        )
        self.username.pack(pady=5, padx=5, fill="x")
        self.url = customtkinter.CTkEntry(
            self.frame,
            placeholder_text=self.entry.url,
            width=self.width
        )
        self.url.pack(pady=5, padx=5, fill="x")

        self.email = customtkinter.CTkEntry(
            self.frame,
            placeholder_text=self.entry.email,
            width=self.width
        )
        self.email.pack(pady=5, padx=5, fill="x")

        self.password = customtkinter.CTkEntry(
            self.frame,
            placeholder_text=self.entry.password,
            width=self.width
        )
        self.password.pack(pady=5, padx=5, fill="x")

        self.confirm_button = customtkinter.CTkButton(
            master=self.frame,
            text="Confirm",
            width=150,
            command=self.add_entry,
        )
        self.confirm_button.pack(pady=5, padx=5, fill="x", side="left")
        self.cancel_button = customtkinter.CTkButton(
            master=self.frame,
            text="Cancel",
            width=150,
            command=self.destroy,
        )
        self.cancel_button.pack(pady=5, padx=5, fill="x", side="right")

    def add_entry(self):
        service = self.service.get() if self.service.get() != "" else self.entry.service
        username = self.username.get() if self.username.get() != "" else self.entry.username
        url = self.url.get() if self.url.get() != "" else self.entry.url
        email = self.email.get() if self.email.get() != "" else self.entry.email
        password = self.password.get() if self.password.get() != "" else self.entry.password

        self.controller.interface.update_entry(
            self.entry.id, service, username, url, email, password)
        self.destroy()
        self.update_results()

    def update_results(self):
        self.clear_results()
        results = self.controller.interface.get_all_entries()

        for _, result in enumerate(results):
            create_entry(
                result,
                self.entry_list,
                self.controller
            )

    def clear_results(self):
        for widget in self.entry_list.winfo_children():
            if isinstance(widget, EntryItem):
                widget.destroy()


class ConfirmDialog(customtkinter.CTkToplevel):
    def __init__(self, entry_id, entry_list, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.entry_list = entry_list
        self.entry_id = entry_id
        self.widht = 130
        self.geometry("400x300")
        self.title(f"Delete Entry: {self.entry_id}")

        self.frame = customtkinter.CTkFrame(self)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame.grid(ipadx=10, ipady=10, row=0, column=0, sticky="")

        self.msg = customtkinter.CTkLabel(
            self.frame,
            text="Willst du das wicklich löschen Vadda?",
            width=self.widht
        )
        self.msg.pack(padx=10, pady=10, fill="x")
        self.confirm_button = customtkinter.CTkButton(
            master=self.frame,
            text="Confirm",
            width=150,
            command=self.confirm
        )
        self.confirm_button.pack(pady=5, padx=(10, 5), fill="x", side="left")
        self.cancel_button = customtkinter.CTkButton(
            master=self.frame,
            text="Cancel",
            width=150,
            command=self.destroy
        )
        self.cancel_button.pack(pady=5, padx=(5, 10), fill="x", side="right")

    def confirm(self):
        self.controller.interface.del_entry(self.entry_id)
        self.update_results()

    def update_results(self):
        self.clear_results()
        results = self.controller.interface.get_all_entries()

        for _, result in enumerate(results):
            create_entry(
                result,
                self.entry_list,
                self.controller
            )

    def clear_results(self):
        for widget in self.entry_list.winfo_children():
            if isinstance(widget, EntryItem):
                widget.destroy()


class Searchbar(customtkinter.CTkFrame):
    def __init__(self, entry_list, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.entry_list = entry_list
        self.search_field = customtkinter.CTkEntry(
            master=self,
            placeholder_text="Search",
        )
        self.search_field.pack(
            pady=10, padx=10, fill="x", expand=True, side="left")

        self.search_field.bind("<KeyRelease>", self.update_results)

    def update_results(self, event):
        query = self.search_field.get()
        self.clear_results()

        if query == "":
            results = self.controller.interface.get_all_entries()
        elif len(query) < 3:
            return
        elif query:
            results = self.controller.interface.search_entry(query)

        for _, result in enumerate(results):
            create_entry(
                result,
                self.entry_list,
                self.controller
            )

    def clear_results(self):
        for widget in self.entry_list.winfo_children():
            if isinstance(widget, EntryItem):
                widget.destroy()


def create_entry(entry, parent, controller):
    item_frame = EntryItem(
        entry,
        parent,
        controller,
        height=50,
        border_color="grey",
        border_width=1
    )
    item_frame.pack(fill="x", padx=1, pady=1)
