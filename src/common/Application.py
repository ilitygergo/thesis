import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from .Image import Image


class Application(tk.Frame):
    title = 'Thesis - Grayscale image thinning'
    width = 1000
    height = 600
    imageSrcLabel = tk.Label
    canvas = tk.Canvas
    photo = tk.PhotoImage

    def __init__(self, master=None):
        super().__init__(master)
        master.title(self.title)
        master.minsize(width=self.width, height=self.height)
        master.maxsize(width=self.width, height=self.height)
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        self.pack()
        self.addImageSelectButton()
        self.displayImagePathLabel()
        self.displayImage()

    def displayImagePathLabel(self):
        if Image.getInstance() is None:
            self.imageSrcLabel = tk.Label()
            self.imageSrcLabel.pack()
        else:
            self.imageSrcLabel.config(text=Image.getInstance().path)

    def displayImage(self):
        img = Image.getInstance()
        if img is None:
            self.canvas = tk.Canvas(self.master)
            self.canvas.pack()
        else:
            self.photo = tk.PhotoImage(file=img.path)
            self.canvas.config(width=img.colSize, height=img.rowSize)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

    def addImageSelectButton(self):
        selectImage = tk.Button(self)
        selectImage['text'] = 'Select image'
        selectImage['command'] = self.selectImage
        selectImage.pack(side='bottom')

    def selectImage(self):
        imagePath = self.getImagePathFromDialog()
        if not imagePath:
            return

        if Image.isValidImagePath(imagePath):
            Image.getInstance(imagePath)
            self.refresh()
        else:
            messagebox.showerror('Error', 'Image extension is not supported')

    @staticmethod
    def getImagePathFromDialog():
        return filedialog.askopenfilename(
            initialdir='./common/files/input',
            title='Select A File',
            filetype=(('image files', '*.jpg *.png'), ('all files', '*.*'))
        )

    def refresh(self):
        self.destroy()
        self.__init__(self.master)
