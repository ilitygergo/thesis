import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from .Image import Image


class Application(tk.Frame):
    title = 'Thesis - Grayscale image thinning'
    width = 600
    height = 350
    menu = tk.Menu
    imageSrcLabel = tk.Label
    imageSizeLabel = tk.Label
    canvas = tk.Canvas
    photo = tk.PhotoImage

    def __init__(self, master=None):
        super().__init__(master)
        master.title(self.title)
        master.minsize(width=self.width, height=self.height)
        master.maxsize(width=self.width, height=self.height)
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        master.configure(bg='#CECECE')
        self.displayMenu()
        self.displayImage()
        self.displayImageDetails()

    def displayMenu(self):
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)

        fileMenu = tk.Menu(self.master)
        fileMenu.add_command(label='Select image', command=self.selectImage)
        self.menu.add_cascade(label='File', menu=fileMenu)

        algorithmMenu = tk.Menu(self.master)
        algorithmMenu.add_command(label='Dyer Rosenfeld', command=self.selectImage)
        algorithmMenu.add_command(label='Salari Siy', command=self.selectImage)
        algorithmMenu.add_command(label='Kang Et Al', command=self.selectImage)
        algorithmMenu.add_command(label='Kim', command=self.selectImage)
        algorithmMenu.add_command(label='Couprie Et Al', command=self.selectImage)
        self.menu.add_cascade(label='Algorithm', menu=algorithmMenu)

    def displayImage(self):
        img = Image.getInstance()
        if img is None:
            self.canvas = tk.Canvas(self.master)
            self.canvas.config(bg='#CECECE', highlightbackground='#CECECE')
            self.canvas.grid(row=0, column=0)
        else:
            self.photo = tk.PhotoImage(file=img.path)
            self.canvas.config(width=img.colSize, height=img.rowSize, highlightbackground='black')
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

    def displayImageDetails(self):
        img = Image.getInstance()
        if img is None:
            self.imageSrcLabel = tk.Label()
            self.imageSrcLabel.config(bg='#CECECE')
            self.imageSrcLabel.grid(row=1, column=0)
            self.imageSizeLabel = tk.Label()
            self.imageSizeLabel.config(bg='#CECECE')
            self.imageSizeLabel.grid(row=2, column=0)
        else:
            self.imageSrcLabel.config(text=img.name)
            sizeString = str(img.rowSize) + ' x ' + str(img.colSize)
            self.imageSizeLabel.config(text=sizeString)

    def selectImage(self):
        imagePath = self.getImagePath()
        if not imagePath:
            return

        if Image.isValidImagePath(imagePath):
            Image.getInstance(imagePath)
            self.refreshWindow()
        else:
            messagebox.showerror('Error', 'Image extension is not supported')

    @staticmethod
    def getImagePath():
        return filedialog.askopenfilename(
            initialdir='./common/files/input',
            title='Select A File',
            filetype=(('image files', '*.jpg *.png'), ('all files', '*.*'))
        )

    def refreshWindow(self):
        self.destroy()
        self.__init__(self.master)
