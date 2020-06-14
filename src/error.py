

import tkinter as tk


def ERROR(msg):
    top = tk.Toplevel()
    top.geometry('500x100')
    top.title('Error')
    m1 = tk.Label(top, text='OMG...', font=("Courier", 20), fg='ivory4')
    m2 = tk.Label(top, text='Something went wrong...',
                  font=("Courier", 20), fg='ivory4')
    m1.pack()
    m2.pack()
    err = tk.Label(top, text="Detailed Error: "+msg,
                   font=("Courier", 10), fg='ivory4')
    err.pack()
