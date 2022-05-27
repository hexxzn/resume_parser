import tkinter as tk
from tkinter import BooleanVar, ttk, messagebox

from data import insert

# Pass URL to Insert Function
def submit():
    try:
        insert(entry_url.get(), manual_login.get())
    except Exception as error:
        print(error)
        messagebox.showerror(title='Error', message=error)
    window.destroy()

# Parser Window
window = tk.Tk()
logo = tk.PhotoImage(file='resources/sourceflow.png')
window.iconphoto(False, logo)
window.title('Indeed Resume Extractor')
window.bind('<Return>', submit)
window.resizable(width=False, height=False)
frame_main = ttk.Frame(master=window)
frame_main.grid(padx=10, pady=10)

# Resume URL Label, Entry
label_url = ttk.Label(master=frame_main, text='Resume URL:', border=1)
label_url.grid(row=0, column=0, pady=(0, 10), sticky='w')
entry_url = ttk.Entry(master=frame_main, width=35)
entry_url.grid(row=0, column=1, padx=(10, 0), pady=(0, 10))

# Manual Login Checkbox
manual_login = BooleanVar(value=False)
checkbutton_manual_login = ttk.Checkbutton(master=frame_main, text='Manual Login', variable=manual_login)
checkbutton_manual_login.grid(row=1, column=0, sticky='se')

# Submit Button
button_submit = ttk.Button(master=frame_main, text='Extract', width=10, command=submit)
button_submit.grid(row=1, column=1, sticky='e')

window.mainloop()