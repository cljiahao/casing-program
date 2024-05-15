from tkinter import END, messagebox
from tkinter import Button, Entry, Label, StringVar, Toplevel

from apis.api_container import get_empty, set_empty_cont
from utils.read_write import write_json
from utils.tkinter_utils import clear_value, cont_id


class ContainerSwitch(Toplevel):
    def __init__(self, containers, lot_no):
        Toplevel.__init__(self)
        self.protocol("WM_DELETE_WINDOW", self.exit)
        self.initialize(containers, lot_no)
        self.win_config()
        self.widgets()
        self.grab_set()
        self.mainloop()

    def initialize(self, containers, lot_no):
        self.containers = containers
        self.lot_no = lot_no
        self.res = False
        self.chg_cnt = 0

    def exit(self):
        self.destroy()
        self.quit()

    def reset(self, widget, widget2=False):
        widget.after_idle(lambda: clear_value(widget))
        if widget2:
            widget2.after_idle(lambda: clear_value(widget2))
        widget.focus()

    def cb_entry(self, input, name):
        key = name.split(".")[-1]
        if len(input) == 10:
            match key:
                case "new":
                    error = ""
                    if get_empty(input):
                        if not messagebox.askyesno(
                            title="Reset Container if not empty",
                            message="Is Container Empty?",
                        ):
                            set_empty_cont(input)
                        else:
                            self.reset(self.new_entry)
                            return False
                    else:
                        error = "Container ID not found in system."

                    if error:
                        messagebox.showerror(title=error, message=error)
                        self.reset(self.new_entry)
                        return False
                case "old":
                    curr_conts = self.containers[self.lot_no]
                    if input in curr_conts:
                        self.new_entry.focus()
                    else:
                        messagebox.showerror(
                            title="Container not found",
                            message="Please Check if Container has reels.",
                        )
                        self.reset(self.old_entry)
                        return False
        return True

    def switch_cont(self, old, new):
        self.error.grid_forget()
        old_value = old.get()
        new_value = new.get()
        self.reset(self.old_entry, self.new_entry)
        curr_conts = self.containers[self.lot_no]
        if old_value in curr_conts:

            self.changed.config(
                text=f"Old Container {old_value} <=> New Container {new_value}"
            )
            self.changed.grid(row=3 + self.chg_cnt, column=0, columnspan=4)
            self.chg_cnt += 1

            self.containers[self.lot_no][new_value] = self.containers[self.lot_no][
                old_value
            ]
            del self.containers[self.lot_no][old_value]
            write_json("./config/json/containers.json", self.containers)
            self.res = True
            return
        self.error.config(
            text=f"{old_value} not found\n in previous scanned containers"
        )
        self.error.grid(row=2, column=2, columnspan=2)
        return

    def win_config(self):
        self.title("Switch Containers")
        screen_size = {
            "h_screen": self.winfo_screenheight(),
            "w_screen": self.winfo_screenwidth(),
        }
        self.config(bg="lightgrey", bd=50)
        self.geometry(
            f"{int(screen_size['w_screen']/3)}x{int(screen_size['h_screen']/3)}+{int(screen_size['w_screen']/3)}+{int(screen_size['h_screen']*1/8)}"
        )
        self.reg_entry = (self.register(self.cb_entry), "%P", "%W")
        self.rowconfigure(5, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(4, weight=1)

    def widgets(self):

        Label(self, text="Old Container", background="lightgrey").grid(row=0, column=1)
        old = StringVar()
        self.old_entry = Entry(
            self,
            textvariable=old,
            name="old",
            validate="key",
            validatecommand=self.reg_entry,
        )
        self.old_entry.grid(row=0, column=2, columnspan=2, ipady=3, pady=3)

        Label(self, text="New Container", background="lightgrey").grid(row=1, column=1)
        new = StringVar()
        self.new_entry = Entry(
            self,
            textvariable=new,
            name="new",
            validate="key",
            validatecommand=self.reg_entry,
        )
        self.new_entry.grid(row=1, column=2, columnspan=2, ipady=3, pady=3)

        self.error = Label(self, bg="#fa6464")
        self.changed = Label(self)

        Button(
            self,
            text="Switch",
            command=lambda: self.switch_cont(old, new),
        ).grid(row=6, column=2, columnspan=2, pady=7)
