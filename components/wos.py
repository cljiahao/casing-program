from tkinter import Button, Label, LabelFrame, Entry
from tkinter import CENTER, NS, EW, W

from utils.tkinter_utils import clear_value


labels = [
    {"name": "Machine No", "key": "mcNo", "value": "01", "type": "label"},
    {"name": "Operator ID", "key": "OptCode", "value": "", "type": "entry"},
    {"name": "Lot No", "key": "lotNo", "value": "", "type": "entry"},
    {"name": "Container ID", "key": "contid", "value": "", "type": "entry"},
    {"name": "Reel Barcode ID", "key": "Reelid", "value": "", "type": "entry"},
    {"name": "Inspection No", "key": "inspectionNo", "value": "", "type": "label"},
    {"name": "No of Reels", "key": "noOfReel", "value": "", "type": "label"},
    {"name": "Murata Type", "key": "Item", "value": "", "type": "label"},
    {"name": "Container Count", "key": "noOfBox", "value": "", "type": "label"},
    {"name": "Qty of Finished Goods", "key": "chipQty", "value": "", "type": "label"},
]


def delete(widget):
    widget.after_idle(lambda: clear_value(widget))
    widget.focus()


def wos_gui(frame, reg_entry):

    wos_frame = LabelFrame(
        frame, name="wos", text="WOS Information (Lot Key In)", font=("Calibri", "20")
    )
    wos_frame.rowconfigure(0, weight=1)
    wos_frame.rowconfigure(len(labels) + 1, weight=1)
    wos_frame.columnconfigure(0, weight=1)
    wos_frame.columnconfigure(1, weight=2)
    wos_frame.columnconfigure(2, weight=2)
    wos_frame.columnconfigure(3, weight=1)
    wos_frame.grid(row=0, column=1, rowspan=2, sticky=NS + EW)

    wos_entry = {}
    for i, label_dict in enumerate(labels):

        key = label_dict["key"]

        Label(wos_frame, text=f"{label_dict['name']}: ", font=("Calibri", "16")).grid(
            row=i + 1, column=1, ipadx=5, ipady=5, padx=5, pady=5, sticky=W
        )

        if label_dict["type"] == "entry":
            wos_entry[key] = Entry(
                wos_frame,
                name=key.lower(),
                font=("Calibri", "16"),
                justify=CENTER,
                validate="key",
                validatecommand=reg_entry,
            )
            wos_entry[key].insert(0, label_dict["value"])
            Button(
                wos_frame,
                text="x",
                width=2,
                bg="#fa6565",
                font=("Calibri", "12"),
                command=lambda k=key: delete(wos_entry[k]),
            ).grid(row=i + 1, column=3, sticky=W)

        elif label_dict["type"] == "label":
            wos_entry[key] = Label(
                wos_frame,
                text=label_dict["value"],
                font=("Calibri", "16"),
                width=35,
                anchor=W,
            )

        wos_entry[key].grid(
            row=i + 1, column=2, ipadx=5, ipady=5, padx=10, pady=5, sticky=W
        )

    return wos_entry
