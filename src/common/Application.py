import tkinter as tk


class Application(tk.Frame):
    title = 'Thesis - Grayscale image thinning'
    width = 1000
    height = 600

    def __init__(self, master=None):
        super().__init__(master)
        master.title(self.title)
        master.minsize(width=self.width, height=self.height)
        master.maxsize(width=self.width, height=self.height)
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        self.pack()
        self.addSelectImageButton()

    def addSelectImageButton(self):
        selectImage = tk.Button(self)
        selectImage["text"] = 'Select image'
        selectImage["command"] = self.helloWorld
        selectImage.pack(side="bottom")

    @staticmethod
    def helloWorld():
        print('Hello World!')
