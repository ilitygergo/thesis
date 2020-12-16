import tkinter as tk
from tkinter import filedialog
from .Image import Image


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
        self.addImageSelectButton()

    def addImageSelectButton(self):
        selectImage = tk.Button(self)
        selectImage['text'] = 'Select image'
        selectImage['command'] = self.selectImage
        selectImage.pack(side='bottom')

    def selectImage(self):
        image = Image(self.getImageNameFromDialog())

    @staticmethod
    def getImageNameFromDialog():
        return filedialog.askopenfilename(
            initialdir='./common/files/input',
            title='Select A File',
            filetype=(('image files', '*.jpg *.png'), ('all files', '*.*'))
        )
