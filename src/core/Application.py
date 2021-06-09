import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from src.core.AlgorithmFactory import *


class Application(tk.Frame):
    title = 'Thesis - Grayscale image thinning'
    width = 800
    height = 400
    font = 'Courier'
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

        fileMenu = tk.Menu(self.master, tearoff=0)
        fileMenu.add_command(label='Select image', command=self.selectImage)
        self.menu.add_cascade(label='File', menu=fileMenu)

        algorithmMenu = tk.Menu(self.master, tearoff=0)
        algorithmMenu.add_command(label='Dyer Rosenfeld', command=lambda: self.runAlgorithm(DyerRosenfeldFactory()))
        algorithmMenu.add_command(label='Salari Siy', command=lambda: self.runAlgorithm(SalariSiyFactory()))
        algorithmMenu.add_command(label='Kang Et Al', command=lambda: self.runAlgorithm(KangFactory()))
        algorithmMenu.add_command(label='Kim', command=lambda: self.runAlgorithm(KimFactory()))
        algorithmMenu.add_command(label='Couprie Et Al', command=lambda: self.runAlgorithm(CouprieFactory()))
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
            self.imageSrcLabel.config(bg='#CECECE', font=(self.font, 28))
            self.imageSrcLabel.grid(row=1, column=0)
            self.imageSizeLabel = tk.Label()
            self.imageSizeLabel.config(bg='#CECECE', font=(self.font, 32))
            self.imageSizeLabel.grid(row=2, column=0)
        else:
            self.imageSrcLabel.config(text=img.name)
            sizeString = str(img.rowSize) + ' x ' + str(img.colSize)
            self.imageSizeLabel.config(text=sizeString)

    def selectImage(self):
        imagePath = self.getImagePath()
        if not imagePath:
            return

        if Image.isValidImageExtension(imagePath):
            Image.getInstance(imagePath)
            self.refreshWindow()
        else:
            messagebox.showerror('Error', 'Image extension is not supported')

    @staticmethod
    def getImagePath():
        return filedialog.askopenfilename(
            initialdir='./files/input',
            title='Select A File',
            filetypes=[('image files', '*.jpg *.png'), ('all files', '*.*')]
        )

    @staticmethod
    def runAlgorithm(factory: AlgorithmFactory):
        if Image.getInstance() is None:
            messagebox.showerror('Error', 'Select an image first!')
        if not factory:
            raise Exception('Wrong algorithm!')

        factory.runAlgorithm()

    def refreshWindow(self):
        self.destroy()
        self.__init__(self.master)
