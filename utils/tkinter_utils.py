from tkinter import messagebox
from tkinter import NORMAL, END

from apis.api_container import get_empty, set_empty_cont
from apis.api_lot import get_lot_start_data
from utils.read_write import write_json


def clear_value(entry_value):
    entry_value.delete(0, END)
    entry_value.configure(validate="key")


def opt_code(wos_entry, response, input):
    response["OptCode"] = input
    wos_entry["lotNo"].focus()


def lot_no(wos_entry, response, input, containers):
    if len(wos_entry["OptCode"].get()) != 7:
        error = "Please Scan Operator ID First"
        messagebox.showerror(title=error, message=error)
        wos_entry["lotNo"].after_idle(lambda: clear_value(wos_entry["lotNo"]))
        wos_entry["lotNo"].focus()

        return False

    json = get_lot_start_data(input)
    if json["code"] != "0":
        messagebox.showerror(title="Lot Number Error", message=json["message"])
        wos_entry["lotNo"].after_idle(lambda: clear_value(wos_entry["lotNo"]))
        return False

    if input not in containers:
        containers[input] = {}
    for key, value in json["data"].items():
        if key in wos_entry.keys() and "label" in wos_entry[key].winfo_name():
            wos_entry[key].config(text=value)
        if key in response.keys():
            response[key] = value

    wos_entry["contid"].focus()

    return json["data"]["ReelID"]


def cont_id(wos_entry, response, input, containers):

    lotNo = wos_entry["lotNo"].get()
    error = ""

    if lotNo not in containers:
        error = "Please Scan Lot No First."
    if any(
        [
            input != x and len(y) < int(response["reelPerBox"])
            for x, y in containers[lotNo].items()
        ]
    ):
        error = "There are containers not filled."
    elif input not in containers[lotNo]:
        if get_empty(input):
            if not messagebox.askyesno(
                title="Reset Container if not empty",
                message="Is Container Empty?",
            ):
                set_empty_cont(input)
        else:
            error = "Container ID not found in system."

    if error:
        messagebox.showerror(title=error, message=error)
        wos_entry["contid"].after_idle(lambda: clear_value(wos_entry["contid"]))
        wos_entry["contid"].focus()
        return

    if input not in containers[lotNo]:
        containers[lotNo][input] = []

    wos_entry["Reelid"].focus()


def reel_id(wos_entry, response, input, containers, reelid):

    lotNo = wos_entry["lotNo"].get()
    contid = wos_entry["contid"].get()
    error = ""
    clear = False

    if input not in reelid:
        error = "Reel not found in system"

    elif input in containers[lotNo][contid]:
        error = "Reel already scanned in this container."

    elif input in sum(containers[lotNo].values(), []):
        error = "Reel already scanned in another container."

    elif int(response["reelPerBox"]) <= len(containers[lotNo][contid]):
        error = "Scanning more reels to full container"
        clear = True

    if error:
        messagebox.showerror(title=error, message=error)

    else:
        if input not in containers[lotNo][contid]:
            containers[lotNo][contid].append(input)

        write_json("./config/json/containers.json", containers)

        if len(containers[lotNo][contid]) == 20:
            clear = True

    wos_entry["Reelid"].after_idle(lambda: clear_value(wos_entry["Reelid"]))
    wos_entry["Reelid"].focus()
    if clear:
        wos_entry["contid"].after_idle(lambda: clear_value(wos_entry["contid"]))
        wos_entry["contid"].focus()
