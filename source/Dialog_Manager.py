#
# author = Nils Ommen
# date = 12.08.2024
# version = 2.0
# application use = fireboard api access
# 
# Dialog_Manager.py


import tkinter as tk

class HintEntry(tk.Entry):
    def __init__(self, master=None, placeholder='', cnf={}, fg='black', font=("Arial", 12),
                 fg_placeholder='grey50', *args, **kw):
        super().__init__(master=master, cnf=cnf, bg='white', font=font, *args, **kw)
        self.fg = fg
        self.fg_placeholder = fg_placeholder
        self.placeholder = placeholder
        self.bind('<FocusOut>', lambda event: self.fill_placeholder())
        self.bind('<FocusIn>', lambda event: self.clear_box())
        self.fill_placeholder()

    def clear_box(self):
        if not self.get() and super().get():
            self.config(fg=self.fg)
            self.delete(0, tk.END)

    def fill_placeholder(self):
        if not super().get():
            self.config(fg=self.fg_placeholder)
            self.insert(0, self.placeholder)
    
    def get(self):
        content = super().get()
        if content == self.placeholder:
            return ''
        return content

def quit_entrys(entrys, dialog):
    ety_content = []
    for ety in entrys:
        ety_content.append(ety.get())
    
    dialog.destroy()

    return ety_content

### helper simple dialogs ###
def get_car(root):
    return get_entrys(root, ["Funkrufname"])

def get_info(root):
    return get_entrys(root, ["Information"])

def get_line_and_car(root):
    return get_entrys(root, ["Zeile", "Funkrufname"])

def get_line_and_info(root):
    return get_entrys(root, ["Zeile", "Information"])

def get_own_task(root):
    return get_entrys(root, ["Ort", "Straße", "Hausnummer", "Stichwort", "Stichwort Text", "Beschreibung"])

def get_auth_key_from_entry(root):
    return get_entrys(root, ["Auth-Key"])

def handle_return(_dialog, _btn_ok, _btn_cancel):
    if(_dialog.focus_get() == _btn_ok):
        _dialog.quit()
    elif(_dialog.focus_get() == _btn_cancel):
        _dialog.destroy()
        
def get_entrys(root, texts):
    dialog = tk.Toplevel(root)
    dialog.focus_set()
    dialog.bind("<Return>", lambda event: dialog.focus_get().invoke() if isinstance(dialog.focus_get(), tk.Button) else None)
    dialog.bind("<FocusOut>", lambda event: dialog.destroy() if not dialog.focus_get() else None)
    dialog.title("Eingabe")
    
    frm_entrys = tk.Frame(
        master = dialog,
        padx = 10,
        pady = 10,
        width = 300,
        height = 100,
        bg = "white"
    )

    entrys = []
    for text in texts:
        _ety = HintEntry(frm_entrys, 
                         placeholder = text, 
                         font = ("Arial", 20))
        _ety.pack(
            padx = 5,
            pady = 5
        )
        entrys.append(_ety)

    frm_entrys.pack(
        fill = tk.BOTH,
        side = tk.TOP,
        expand = True,
    )

    frm_buttons = tk.Frame(
        master = dialog,
        width = 300,
        height = 60,
        bg = "white"
    )

    btn_ok = tk.Button(
        master = frm_buttons,
        text = "Bestätigen",
        font = ("Arial", 20),
        command = lambda : dialog.quit()
    )
    btn_ok.focus_set()
    btn_ok.pack(
        side = tk.LEFT,
        padx = 5,
        pady = 5,
    )

    btn_cancel = tk.Button(
        master = frm_buttons,
        text = "Abbrechen",
        font = ("Arial", 20),
        command = lambda: dialog.destroy(),
    )
    dialog.bind("<Escape>", lambda event: dialog.destroy())

    btn_cancel.pack(
        side = tk.RIGHT,
        padx = 5,
        pady = 5,
    )

    frm_buttons.pack(
        fill = tk.BOTH,
        side = tk.BOTTOM,
        expand = True,
    )

    dialog.mainloop()

    return quit_entrys(entrys, dialog)