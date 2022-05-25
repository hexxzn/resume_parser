import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from resources.config import email, password
from data import insert

# Pass Entry Information to Insert Function
def submit():
    try:
        email = entry_email.get()
        password = entry_password.get()
        extract_url = entry_url.get()
        insert(email, password, extract_url)
    except Exception as error:
        messagebox.showerror(title='Error', message=error)
        print(error)
    window.destroy()

# Auto Fill Entry With Config Variables
def Auto_Fill(entry, text):
    if text:
        entry.insert(0, text)

# Parser Window

window = tk.Tk()
logo = tk.PhotoImage(file='resources/logo.png')
window.iconphoto(False, logo)
window.title('Indeed Resume Extractor')
window.bind('<Return>', submit)
window.resizable(width=False, height=False)
style = ttk.Style()
style.theme_use('clam')
frame_main = ttk.Frame(master=window)
frame_main.grid(padx=10, pady=10)


# Email Label and Entry
label_email = ttk.Label(master=frame_main, text='Email:')
label_email.grid(row=0, column=0, pady=(0, 10), sticky='w')
entry_email = ttk.Entry(master=frame_main, width=35)
entry_email.grid(row=0, column=1, padx=(10, 0), pady=(0, 10))
Auto_Fill(entry_email, email)

# Password Label and Entry
label_password = ttk.Label(master=frame_main, text='Password:')
label_password.grid(row=1, column=0, pady=(0, 10), sticky='w')
entry_password = ttk.Entry(master=frame_main, width=35)
entry_password.config(show="●")
entry_password.grid(row=1, column=1, padx=(10, 0), pady=(0, 10))
Auto_Fill(entry_password, password)

# Resume URL Label and Entry
label_url = ttk.Label(master=frame_main, text='Resume URL:')
label_url.grid(row=2, column=0, pady=(0, 10), sticky='w')
entry_url = ttk.Entry(master=frame_main, width=35)
entry_url.grid(row=2, column=1, padx=(10, 0), pady=(0, 10))

# Submit Button
button_submit = ttk.Button(master=frame_main, text='Submit', width=10, command=submit)
button_submit.grid(row=3, column=1, padx=(10, 0), sticky='e')

window.mainloop()