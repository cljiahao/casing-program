from tkinter import Tk, Frame, messagebox
from tkinter import BOTH
from datetime import datetime as dt

from apis.api_container import set_empty_cont, update_empty
from apis.api_lot import complete_lot, get_lot_start_data, update_cont
from components.buttons import buttons_gui
from components.containers import cont_gui, cont_id_gui, cont_lot_gui
from components.wos import wos_gui
from pages.ContainerSwitch import ContainerSwitch
from pages.Login import Login
from utils.read_write import read_json, write_dat, write_json
from utils.tkinter_utils import opt_code, cont_id, lot_no, reel_id


class ContainerScan(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.initialize()
        self.win_config()
        self.widgets()

    def initialize(self):
        self.response = {
            "lotNo": "",
            "Item": "",
            "inspectionNo": "",
            "chipQty": "",
            "noOfReel": "",
            "reelPerBox": "",
            "noOfBox": "",
            "OptCode": "",
            "Contid": [],
        }
        self.containers = read_json("./config/json/containers.json")

    def cb_entry(self, input, name):
        """Call backs for Entry"""
        key = name.split(".")[-1]
        match key:
            case "optcode":
                if len(input) == 7:
                    opt_code(self.wos_entry, self.response, input)

            case "lotno":
                if len(input) == 10:
                    self.reedid = lot_no(
                        self.wos_entry, self.response, input, self.containers
                    )
                    if self.reedid:
                        cont_lot_gui(self.cont_frame, input)
                        cont_id_gui(self.cont_frame, self.containers[input])

            case "contid":
                if len(input) == 10:
                    cont_id(self.wos_entry, self.response, input, self.containers)
                    cont_id_gui(
                        self.cont_frame,
                        self.containers[self.wos_entry["lotNo"].get()],
                    )

            case "reelid":
                if len(input) == 15:
                    reel_id(
                        self.wos_entry,
                        self.response,
                        input,
                        self.containers,
                        self.reedid,
                    )
                    cont_id_gui(
                        self.cont_frame,
                        self.containers[self.wos_entry["lotNo"].get()],
                    )

        return True

    def reset(self):
        for widget in self.frame.winfo_children():
            if widget.winfo_name() in ["wos", "container"]:
                widget.destroy()

        self.initialize()
        self.wos_entry = wos_gui(self.frame, self.reg_entry)
        self.cont_frame = cont_gui(self.frame)

    def switch(self):
        status = Login().res
        if status:
            lot_no = self.wos_entry["lotNo"].get()
            if lot_no in self.containers:
                res = ContainerSwitch(self.containers, lot_no).res
                if res:
                    cont_id_gui(self.cont_frame, self.containers[lot_no])

    def refresh(self):
        lot_no = self.wos_entry["lotNo"].get()
        if not lot_no:
            return
        json = get_lot_start_data(lot_no)

        for cont, reels in self.containers[lot_no].items():
            for reel in reels:
                if reel not in json["data"]["ReelID"]:
                    self.containers[lot_no][cont].remove(reel)

        write_json("./config/json/containers.json", self.containers)
        cont_id_gui(self.cont_frame, self.containers[lot_no])

    def end_lot(self):
        lot_no = self.wos_entry["lotNo"].get()

        if lot_no not in self.containers:
            return

        contids = self.containers[lot_no]
        for i, contid in enumerate(contids.keys()):
            temp_cont = {
                "contid": contid,
                "contSeq": f"{(i + 1) / 1000:.3f}".split(".")[-1],
                "Reelid": [],
            }
            for j, reelid in enumerate(contids[contid]):
                temp_cont["Reelid"].append(
                    {"id": reelid, "seq": f"{(j + 1) / 100:.2f}".split(".")[-1]}
                )

            self.response["Contid"].append(temp_cont)

        res = complete_lot(self.response)
        if res["code"] != "0":
            messagebox.showinfo(title="Error for Lot End", message=res["message"])
            return
        for contid in self.containers[lot_no]:
            set_empty_cont(contid)
        #     dat_str = f"S20|{dt.now().strftime('%Y/%m/%d %H:%M:%S')}|{self.response["OptCode"]}|{contid}|1"
        #     dat_path = f"./data/{contid}.dat"
        #     write_dat(dat_path, dat_str)
        #     update_cont(dat_path)

        messagebox.showinfo(title="Lot Ended", message="Lot ended successfully.")
        del self.containers[lot_no]
        write_json("./config/json/containers.json", self.containers)
        self.reset()

    def win_config(self):
        self.title("Casing Scan")
        self.state("zoomed")
        self.frame = Frame(self)
        self.frame.rowconfigure(0, weight=15, uniform="a")
        self.frame.rowconfigure(1, weight=2, uniform="a")
        for i in range(5):
            weight = 1 if i % 2 == 0 else 10
            self.frame.columnconfigure(i, weight=weight, uniform="a")
        self.frame.columnconfigure(1, weight=17, uniform="a")
        self.frame.pack(fill=BOTH, expand=True, pady=30)
        self.reg_entry = (self.register(self.cb_entry), "%P", "%W")
        self.button_info = {
            "reset": {"text": "Reset", "onClick": self.reset},
            "switch": {"text": "Switch", "onClick": self.switch},
            "refresh": {"text": "Refresh", "onClick": self.refresh},
            "lotend": {"text": "Lot End", "onClick": self.end_lot},
        }

    def widgets(self):

        self.wos_entry = wos_gui(self.frame, self.reg_entry)

        self.cont_frame = cont_gui(self.frame)

        buttons_gui(self.frame, self.button_info)
