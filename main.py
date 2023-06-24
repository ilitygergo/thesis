import tkinter as tk
import traceback

from src.core import Application

try:
    root = tk.Tk()
    app = Application.Application(master=root)
    app.mainloop()
except Exception:
    print(traceback.format_exc())
