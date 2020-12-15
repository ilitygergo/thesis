import time
import tkinter as tk
from common import Application
from common import Image

# startTime = time.time()

try:
    root = tk.Tk()
    app = Application.Application(master=root)
    app.mainloop()
except Exception as e:
    print(e)

# endTime = time.time()
# print(endTime - startTime)
