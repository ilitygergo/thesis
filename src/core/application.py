import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from src.core.algorithm_factory import (
    AlgorithmFactory,
    CouprieFactory,
    DyerRosenfeldFactory,
    KangFactory,
    KimFactory,
    SalariSiyFactory,
)
from src.thinning.image import Image


class Application(tk.Frame):
    title: str = "Thesis - Grayscale image thinning"
    width: int = 800
    height: int = 400
    font: str = "Courier"
    menu: tk.Menu = tk.Menu
    imageSrcLabel: tk.Label = tk.Label
    imageSizeLabel: tk.Label = tk.Label
    canvas: tk.Canvas = tk.Canvas
    photo: tk.PhotoImage = tk.PhotoImage

    def __init__(self, master=None):
        super().__init__(master)
        master.title(self.title)
        master.minsize(width=self.width, height=self.height)
        master.maxsize(width=self.width, height=self.height)
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        master.configure(bg="#CECECE")
        self.display_menu()
        self.display_image()
        self.display_image_details()

    def display_menu(self):
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)

        fileMenu = tk.Menu(self.master, tearoff=0)
        fileMenu.add_command(label="Select image", command=self.select_image)
        self.menu.add_cascade(label="File", menu=fileMenu)

        algorithmMenu = tk.Menu(self.master, tearoff=0)
        algorithmMenu.add_command(
            label="Dyer Rosenfeld",
            command=lambda: self.run_algorithm(DyerRosenfeldFactory()),
        )
        algorithmMenu.add_command(
            label="Salari Siy", command=lambda: self.run_algorithm(SalariSiyFactory())
        )
        algorithmMenu.add_command(
            label="Kang Et Al", command=lambda: self.run_algorithm(KangFactory())
        )
        algorithmMenu.add_command(
            label="Kim", command=lambda: self.run_algorithm(KimFactory())
        )
        algorithmMenu.add_command(
            label="Couprie Et Al", command=lambda: self.run_algorithm(CouprieFactory())
        )
        self.menu.add_cascade(label="Algorithm", menu=algorithmMenu)

    def display_image(self):
        img = Image.getInstance()
        if img is None:
            self.canvas = tk.Canvas(self.master)
            self.canvas.config(bg="#CECECE", highlightbackground="#CECECE")
            self.canvas.grid(row=0, column=0)
        else:
            self.photo = tk.PhotoImage(file=img.path)
            self.canvas.config(
                width=img.colSize, height=img.rowSize, highlightbackground="black"
            )
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

    def display_image_details(self):
        img = Image.getInstance()
        if img is None:
            self.imageSrcLabel = tk.Label()
            self.imageSrcLabel.config(bg="#CECECE", font=(self.font, 28))
            self.imageSrcLabel.grid(row=1, column=0)
            self.imageSizeLabel = tk.Label()
            self.imageSizeLabel.config(bg="#CECECE", font=(self.font, 32))
            self.imageSizeLabel.grid(row=2, column=0)
        else:
            self.imageSrcLabel.config(text=img.name)
            sizeString = str(img.rowSize) + " x " + str(img.colSize)
            self.imageSizeLabel.config(text=sizeString)

    def select_image(self):
        imagePath = self.get_image_path()
        if not imagePath:
            return

        if Image.isValidImageExtension(imagePath):
            Image.getInstance(imagePath)
            self.refresh_window()
        else:
            messagebox.showerror("Error", "Image extension is not supported")

    @staticmethod
    def get_image_path():
        return filedialog.askopenfilename(
            initialdir="./assets/input",
            title="Select A File",
            filetypes=[("image files", "*.jpg *.png"), ("all files", "*.*")],
        )

    @staticmethod
    def run_algorithm(factory: AlgorithmFactory):
        loading_screen = Application.init_loading_screen()

        if Image.getInstance() is None:
            messagebox.showerror("Error", "Select an image first!")
        if not factory:
            raise Exception("Wrong algorithm!")

        factory.run_algorithm(loading_screen)
        loading_screen.withdraw()

    @staticmethod
    def init_loading_screen() -> tk.Tk:
        loading_screen = tk.Tk()
        tk.Label(loading_screen, text="Running algorithm...").pack()
        pb = ttk.Progressbar(loading_screen, length=200, mode="indeterminate")
        pb.pack()
        pb.start()

        return loading_screen

    def refresh_window(self):
        self.destroy()
        self.__init__(self.master)
