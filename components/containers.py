from tkinter import Label, LabelFrame, Frame
from tkinter import NS, EW, E, W


def cont_gui(frame):

    cont_frame = LabelFrame(
        frame, name="container", text="Container Information", font=("Calibri", "20")
    )
    cont_frame.rowconfigure(0, weight=1, uniform="a")
    cont_frame.rowconfigure(1, weight=2, uniform="a")
    cont_frame.rowconfigure(2, weight=20, uniform="a")
    cont_frame.rowconfigure(3, weight=2, uniform="a")
    cont_frame.columnconfigure(0, weight=1, uniform="a")
    cont_frame.columnconfigure(1, weight=7, uniform="a")
    cont_frame.columnconfigure(2, weight=1, uniform="a")
    cont_frame.grid(row=0, column=3, sticky=NS + EW)

    cont_lot_gui(cont_frame, "")
    cont_id_gui(cont_frame, {})

    return cont_frame


def cont_lot_gui(cont_frame, lot_no):

    for widget in cont_frame.winfo_children():
        if widget.winfo_name() == "cont_lot":
            widget.destroy()

    cont_lot_frame = Frame(cont_frame, name="cont_lot")
    cont_lot_frame.grid(row=1, column=1, sticky=EW)

    Label(cont_lot_frame, text="Lot No: ", font=("Calibri", "16")).grid(row=1, column=1)
    Label(cont_lot_frame, text=lot_no, font=("Calibri", "16")).grid(row=1, column=2)


def cont_id_gui(cont_frame, containers):

    for widget in cont_frame.winfo_children():
        if widget.winfo_name() == "Containers":
            widget.destroy()

    cont_id_frame = LabelFrame(
        cont_frame, name="cont_id", text="Containers", font=("Calibri", "16")
    )
    cont_id_frame.columnconfigure(0, weight=1, uniform="a")
    cont_id_frame.columnconfigure(1, weight=1, uniform="a")
    cont_id_frame.grid(row=2, column=1, sticky=NS + EW)

    for i, key in enumerate(containers.keys()):
        Label(cont_id_frame, text=key, font=("Calibri", "14")).grid(
            row=i, column=0, padx=20, pady=5, sticky=W
        )
        Label(cont_id_frame, text=len(containers[key]), font=("Calibri", "14")).grid(
            row=i, column=1, padx=20, pady=5, sticky=E
        )
