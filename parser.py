import tkinter as tk
from tkinter import messagebox
from insert import insert

# Pass Entry Information to Insert Function
def submit():
    try:
        email = entry_email.get()
        password = entry_password.get()
        extract_url = entry_link.get()
        insert(email, password, extract_url)
    except Exception as error:
        messagebox.showerror(title='Error', message=error)
        print(error)
    window.destroy()

# Indeed Resume Parser Window
window = tk.Tk()
logo = tk.PhotoImage(file='images/logo.png')
window.title('Indeed Resume Parser')
window.iconphoto(False, logo)
window.bind('<Return>', submit)
window.configure(bg='gray')

# Email Label and Entry
frame_email = tk.Frame(master=window, bg='gray')
frame_email.grid(row=0, column=0, padx=10, pady=10, sticky='w')
label_email = tk.Label(master=frame_email, text='Email:', bg='gray')
label_email.grid(sticky='w')
entry_email = tk.Entry(master=frame_email, width=35)
entry_email.grid()

# Password Label and Entry
frame_password = tk.Frame(master=window, bg='gray')
frame_password.grid(row=1, column=0, padx=10, pady=10, sticky='w')
label_password = tk.Label(master=frame_password, text='Password:', bg='gray')
label_password.grid(sticky='w')
entry_password = tk.Entry(master=frame_password, width=35)
entry_password.grid()

# Resume Link Label and Entry
frame_link = tk.Frame(master=window, bg='gray')
frame_link.grid(row=2, column=0, padx=10, pady=10, sticky='w')
label_link = tk.Label(master=frame_link, text='Resume Link:', bg='gray')
label_link.grid(sticky='w')
entry_link = tk.Entry(master=frame_link, width=35)
entry_link.grid()

# Submit Button
frame_submit = tk.Frame(master=window)
frame_submit.grid(row=3, column=0, padx=10, pady=10, sticky='w')
button_submit = tk.Button(master=frame_submit, text='Submit', width=10, command=submit)
button_submit.grid()

window.mainloop()