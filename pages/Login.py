import subprocess
from tkinter import END
from tkinter import Button, Entry, Label, StringVar, Toplevel

from config.config import settings


class Login(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.initialize()
        self.win_config()
        self.widgets()
        self.grab_set()
        self.mainloop()

    def initialize(self):
        self.res = False
        subprocess.Popen("osk", stdout=subprocess.PIPE, shell=True)

    def check_login(self, user, user_entry, pwd, pwd_entry):
        if settings.USER == user.get():
            if settings.PWD == pwd.get():
                self.res = True
                self.destroy()
                self.quit()
                return
            else:
                self.bad_pass.config(text="Password does not match")
                self.bad_pass.grid(row=2, column=2, columnspan=2)
                pwd_entry.delete(0, END)
                return
        self.bad_pass.config(text="Username does not match")
        self.bad_pass.grid(row=2, column=2, columnspan=2)
        user_entry.delete(0, END)
        user_entry.focus()
        return

    def win_config(self):
        self.title("Login")
        screen_size = {
            "h_screen": self.winfo_screenheight(),
            "w_screen": self.winfo_screenwidth(),
        }
        self.config(bg="#A4C0D6", bd=50)
        self.geometry(
            f"{int(screen_size['w_screen']/4)}x{int(screen_size['h_screen']/4)}+{int(screen_size['w_screen']*3/8)}+{int(screen_size['h_screen']*1/8)}"
        )
        self.rowconfigure(5, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(4, weight=1)

    def widgets(self):

        # Username
        Label(self, text="Username:", background="#A4C0D6").grid(row=0, column=1)
        user = StringVar()
        user_entry = Entry(self, textvariable=user)
        user_entry.grid(row=0, column=2, columnspan=2, ipady=3, pady=3)

        # Password
        Label(self, text="Password:", background="#A4C0D6").grid(row=1, column=1)
        pwd = StringVar()
        pwd_entry = Entry(self, textvariable=pwd)
        pwd_entry.config(show="*")
        pwd_entry.grid(row=1, column=2, columnspan=2, ipady=3, pady=3)

        self.bad_pass = Label(self, bg="#fa6464")

        Button(
            self,
            text="Login",
            command=lambda: self.check_login(user, user_entry, pwd, pwd_entry),
        ).grid(row=6, column=2, columnspan=2, pady=5)
