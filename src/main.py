import tkinter as tk
from core import Application

try:
    root = tk.Tk()
    app = Application.Application(master=root)
    app.mainloop()
except Exception as e:
    print(e)
