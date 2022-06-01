import tkinter as tk
from tkinter import BooleanVar, ttk, messagebox

from extractor import resume_extractor

# Pass url to extractor
def submit(event = None):
    try:
        resume_extractor(entry_url.get(), manual_login.get())
    except Exception as error:
        print(error)
        messagebox.showerror(title='Error', message=error)
    window.destroy()

# Create user interface main window
window = tk.Tk()
logo = tk.PhotoImage(file='resources/sourceflow.png')
window.iconphoto(False, logo)
window.title('Indeed Resume Extractor')
window.bind('<Return>', submit)
window.resizable(width=False, height=False)
frame_main = ttk.Frame(master=window)
frame_main.grid(padx=15, pady=15)

# Create resume URL label and entry
label_url = ttk.Label(master=frame_main, text='Resume URL:', border=1)
label_url.grid(row=0, column=0, pady=(0, 15), sticky='w')
entry_url = ttk.Entry(master=frame_main, width=35)
entry_url.grid(row=0, column=1, pady=(0, 15), sticky='e')

# Create manual login checkbox
manual_login = BooleanVar(value=False)
checkbutton_manual_login = ttk.Checkbutton(master=frame_main, text='Manual Login', variable=manual_login)
checkbutton_manual_login.grid(row=1, column=0, sticky='sw')

# Create extract button
button_extract = ttk.Button(master=frame_main, text='Extract', width=10, command=submit)
button_extract.grid(row=1, column=1, sticky='se')

window.mainloop()