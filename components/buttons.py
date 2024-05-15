from tkinter import Frame, Button
from tkinter import NS, EW


def buttons_gui(frame, button_info):

    button_frame = Frame(frame, name="buttons")
    button_frame.rowconfigure(0, weight=1)
    button_frame.grid(row=1, column=3, sticky=NS + EW)

    for i in range(len(button_info)):
        button_frame.columnconfigure(i, weight=1, uniform="a")

    for j, value in enumerate(button_info.values()):
        button = Button(button_frame, text=value["text"])
        button.grid(row=0, column=j, padx=10, pady=10, sticky=NS + EW)
        if callable(value["onClick"]):
            button.configure(command=lambda value=value: value["onClick"]())
