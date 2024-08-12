#
# author = Nils Ommen
# date = 12.08.2024
# version = 2.0
# application use = fireboard api access
# 
# Window_Manager.py

from Menu import *
from Dialog_Manager import *
import tkinter as tk
from tkinter import messagebox
from Fireboard_Task import set_auth_key

window = tk.Tk()
frames = []

### actions for buttons ### 
def aktion_einsatz_btn():
    if(messagebox.askokcancel("Neuer Einsatz?", "Neuen Einsatz generieren?")):
        create_task_from_pool()
        reload_table()

def aktion_eigener_einsatz_btn():
    town, street, number, msg_short, msg_text, description = get_own_task(window)
    
    # process town street and number to a address
    if town is not None and street is not None and number is not None:
        address = str(town) + ", " + str(street) + " " + str(number)

    if address is not None and msg_short is not None and msg_text is not None:
        create_task(address, msg_short, msg_text, description)
        reload_table()

def aktion_fahrzeug_btn(line):
    car = get_car(window)[0]

    if car is not None and line is not None:
        add_car_func(line, car)
        reload_table()
        cmd_stack.append("fzg " + str(line))

def aktion_status_btn():
    line, car = get_line_and_car(window)
  
    if car is not None and line is not None:
        if line.isdigit():
            line_nr = int(line)
            change_status_func(line_nr, car)
            reload_table()
        else:
            print("[ERROR]: Eingabe war kein Integer.")

def aktion_set_auth_key_btn():
    auth_key = get_auth_key_from_entry(window)[0]
    set_auth_key(auth_key)

def aktion_info_btn(line):
    info = get_info(window)[0]
       
    if info is not None and line is not None:
            add_info_func(line, info)
            reload_table()
            cmd_stack.append("info " + str(line))
        
def aktion_undo_btn():
    if(messagebox.askokcancel("Warnung", "Letzten Befehl rückgängig machen?")):
        undo_func()
        reload_table()

def aktion_exit_btn():
    if(messagebox.askokcancel("Warnung", "Wirklich beenden?")):
        try:    
            window.destroy()
        except:
            pass

        print("[INFO]: Fenster geschlossen.")

### help functions to handle frames ###
def reload_table():
    frames[0].destroy()
    frames[0] = create_table_frame()
    frames[0].pack(
        fill = tk.BOTH,
        side = tk.TOP,
        expand = True,
        padx = 10,
        pady = 10,
    )

def create_button_frame():
    button_text = ["Einsatz", "Eigener Einsatz", "Status", "set Auth-Key", "Undo", "Exit"]
    button_font = ("Arial", 20)
    button_action = [aktion_einsatz_btn, aktion_eigener_einsatz_btn, aktion_status_btn, aktion_set_auth_key_btn, aktion_undo_btn, aktion_exit_btn]

    _frm_buttons = tk.Frame(
        width = 100,
        height = 50,
        master = window,
        bg = "gray"
    )

    for i in range(len(button_text)):
        _frm = tk.Frame(
            master = _frm_buttons,
            relief = tk.RAISED,
            borderwidth = 1
        )
        _frm.grid(row = 0, column = i)
        _btn = tk.Button(
            master = _frm,
            text = button_text[i],
            font = button_font,
            command = button_action[i],
            padx = 20,
            bg = "gray",
            fg = "black"
        )
        _btn.pack() 
    
    # bind button event on return key but only when button is focused
    window.bind("<Return>", lambda event: window.focus_get().invoke() if isinstance(window.focus_get(), tk.Button) else None)
    # bind escape key to exit button event
    window.bind("<Escape>", lambda event: aktion_exit_btn())
    return _frm_buttons

def create_table_frame():
    _table = get_table()
    _frm_table = tk.Frame(
        width = 100,
        height = 50,
        master = window,
        bg = "white"
    )

    # Todo: der Text kann sich natürlich hier ändern..
    column_cars = _table[0].index("Fahrzeuge")
    column_info = _table[0].index("Infos")

    for idx_row in range(len(_table)):
        _frm_table.columnconfigure(list(range(len(_table[0]))), weight=1)
        _frm_table.rowconfigure(idx_row, weight=0, minsize=50)

        for idx_column in range(len(_table[0])):
            _frm = tk.Frame(
                master = _frm_table,
                bg = "white"
            )
            _frm.grid(row = idx_row, column = idx_column, sticky = "nw")
            lbl_cell = tk.Label(
                master = _frm, 
                text = _table[idx_row][idx_column],
                font = ("Arial", 20),
                bg = "white",
                anchor = "w",
                justify = tk.LEFT,
            )
            lbl_cell.pack(padx = 5, pady = 5, side = tk.LEFT)

            if idx_row != 0 and (idx_column == column_cars or idx_column == column_info):
                btn_cell = tk.Button(
                    master = _frm,
                    text = "+",
                    font = ("Arial", 20),
                    relief = tk.GROOVE,
                    borderwidth = 1,
                    bg = "white"
                )
                if(idx_column == column_cars):
                    btn_cell.config(command = lambda row=idx_row : aktion_fahrzeug_btn(row))
                elif(idx_column == column_info):
                    btn_cell.config(command = lambda row=idx_row : aktion_info_btn(row))
                else:
                    print("[ERROR]: cannot find a matching function for this button")

                btn_cell.pack(side = tk.LEFT)

    return _frm_table

### main window create function ###
def window_create():
    window.configure(bg = "white")

    frm_table = create_table_frame()
    frm_buttons = create_button_frame()

    frm_table.pack(
        fill = tk.BOTH,
        side = tk.TOP,
        expand = True,
        padx = 10,
        pady = 10,
    )

    frames.append(frm_table)

    frm_buttons.pack(
        fill = tk.BOTH,
        side = tk.BOTTOM,
        expand = False,
    )

    frames.append(frm_buttons)
    #window.attributes("-fullscreen", True) 
    window.mainloop()