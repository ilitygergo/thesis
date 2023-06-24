import tkinter as tk
import traceback

from src.core.application import Application

try:
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
except Exception:
    print(traceback.format_exc())
