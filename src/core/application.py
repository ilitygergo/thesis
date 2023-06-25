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
    width: int = 1000
    height: int = 600
    font: str = "Modern"
    menu = tk.Menu
    image_src_label = tk.Label
    image_size_label = tk.Label
    canvas = tk.Canvas
    photo = tk.PhotoImage

    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master)
        self.master = master
        self.master.title(self.title)
        self.master.minsize(width=self.width, height=self.height)
        self.master.maxsize(width=self.width, height=self.height)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.configure(bg="#CECECE")

        self.display_menu()
        self.display_image()
        self.display_image_details()

    def display_menu(self) -> None:
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)

        fileMenu = tk.Menu(self.master, tearoff=0)
        fileMenu.add_command(label="Select image", command=self.select_image)
        self.menu.add_cascade(label="File", menu=fileMenu)

        algorithmMenu = tk.Menu(self.master, tearoff=0)
        algorithmMenu.add_command(
            label="Dyer Rosenfeld",
            command=lambda: self.run(DyerRosenfeldFactory()),
        )
        algorithmMenu.add_command(
            label="Salari Siy", command=lambda: self.run(SalariSiyFactory())
        )
        algorithmMenu.add_command(
            label="Kang Et Al", command=lambda: self.run(KangFactory())
        )
        algorithmMenu.add_command(label="Kim", command=lambda: self.run(KimFactory()))
        algorithmMenu.add_command(
            label="Couprie Et Al", command=lambda: self.run(CouprieFactory())
        )
        self.menu.add_cascade(label="Algorithm", menu=algorithmMenu)

    def display_image(self) -> None:
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

    def display_image_details(self) -> None:
        img = Image.getInstance()
        if img is None:
            self.image_src_label = tk.Label()
            self.image_src_label.config(bg="#CECECE", font=(self.font, 28))
            self.image_src_label.grid(row=1, column=0)
            self.image_size_label = tk.Label()
            self.image_size_label.config(bg="#CECECE", font=(self.font, 32))
            self.image_size_label.grid(row=2, column=0)
        else:
            self.image_src_label.config(text=img.name)
            size_string = str(img.rowSize) + " x " + str(img.colSize)
            self.image_size_label.config(text=size_string)

    def select_image(self) -> None:
        imagePath = self.get_image_path("./assets/input")
        if not imagePath:
            return

        if Image.isValidImageExtension(imagePath):
            Image.getInstance(imagePath)
            self.refresh_window()
        else:
            messagebox.showerror("Error", "Image extension is not supported")

    def get_image_path(self, init_dir: str) -> str:
        return filedialog.askopenfilename(
            initialdir=init_dir,
            title="Select A File",
            filetypes=[("image files", "*.jpg *.png"), ("all files", "*.*")],
        )

    def run(self, factory: AlgorithmFactory) -> None:
        loading_screen = self._init_loading_screen()

        if Image.getInstance() is None:
            messagebox.showerror("Error", "Select an image first!")
        if not factory:
            raise Exception("Wrong algorithm!")

        factory.run_algorithm(loading_screen)
        loading_screen.withdraw()

    def _init_loading_screen(self) -> tk.Tk:
        loading_screen = tk.Tk()
        tk.Label(loading_screen, text="Running algorithm...").pack()
        pb = ttk.Progressbar(loading_screen, length=200, mode="indeterminate")
        pb.pack()
        pb.start()

        return loading_screen

    def refresh_window(self) -> None:
        self.destroy()
        self.__init__(self.master)
