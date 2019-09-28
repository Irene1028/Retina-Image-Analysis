import os.path
import sys
import PIL
#from PIL import Image, ImageTk
import PIL.Image
import PIL.ImageMath
import PIL.ImageTk
import PIL.ImageDraw
import PIL.ImageChops
import PIL.ImageFilter
from tkinter import *
from tkinter import filedialog as tkFileDialog
# import tkFileDialog
import scipy
import scipy.fftpack
import scipy.ndimage
import numpy as np
import inspect
import matplotlib.pyplot as plt
from dialog_window import dialog_window
from tools import morph_elemt
# logger=True


class Imagewindow:
    def __init__(self, master):
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.geometry('800x500')
        self.img = PIL.Image.new('L', (800, 500))   # create greyscale img
        self.gimg = PIL.Image.new('L', (800, 500))  # create greyscale gimg
        self.bimg = PIL.Image.new('1', (800, 500))  # create a-bit bimg (black and white)
        self.master.title("Retinal Image Processor")
        self.filename = ""
        """Undo init"""
        self.max_undos = 6
        self.undolist = []

        menuBar = Menu(self.master)
        self.master.config(menu=menuBar)

        """File"""
        fileBar = Menu(menuBar)
        fileBar.add_command(label="Open", command=self.openfile)
        fileBar.add_command(label="Save as", command=self.savefile)
        fileBar.add_command(label="Quit", command=self.master.destroy)
        menuBar.add_cascade(label="File", menu=fileBar)

        """Edit"""
        editBar = Menu(menuBar)
        # TODO: Add Undo.
        editBar.add_command(label="Undo", command=self.undo)
        menuBar.add_cascade(label="Edit", menu=editBar)

        """Operations"""
        """ This bar include different filters used for noise reduction """
        opBar = Menu(menuBar)
        # Filters
        filterMenu = Menu(opBar)
        filterMenu.add_command(label="Median Blur", command=self.master.destroy)
        filterMenu.add_command(label="Augmentation", command=self.master.destroy)
        filterMenu.add_command(label="Blur", command=self.master.destroy)
        filterMenu.add_command(label="Edge Enhance", command=self.master.destroy)
        opBar.add_cascade(label="Filters", menu=filterMenu)
        # Morphology
        morphMenu = Menu(opBar)
        morphMenu.add_command(label="Erosion", command=lambda: self.morph_helper("Erosion"))
        morphMenu.add_command(label="Dilation", command=lambda: self.morph_helper("Dilation"))
        morphMenu.add_command(label="Opening", command=lambda: self.morph_helper("Opening"))
        morphMenu.add_command(label="Closing", command=lambda: self.morph_helper("Closing"))
        opBar.add_cascade(label="Morphology", menu=morphMenu)

        menuBar.add_cascade(label="Operations", menu=opBar)

        """Analysis"""
        analysisBar = Menu(menuBar)
        # TODO: Add counter here.
        analysisBar.add_command(label="Count Cell Numbers", command=self.master.destroy)
        menuBar.add_cascade(label="Analysis", menu=analysisBar)

        """Show Img"""
        image1 = PIL.ImageTk.PhotoImage(self.img)
        self.label_image = Label(self.master, image=image1)

        self.label_image.pack(side="bottom", fill="both", expand="yes")
        self.master.mainloop()

    def openfile(self):
        self.filename = tkFileDialog.askopenfilename(title="Select an Image",
                                                     filetypes=(("jpg files", "*.jpg"), ("all files", "*.*")))
        self.gimg = PIL.Image.open(self.filename).convert("L")
        fhead, ftail = os.path.split(self.filename)
        self.filename = ftail
        self.update()

    def savefile(self):
        filename = tkFileDialog.asksaveasfilename()
        filename += ".jpg"
        self.gimg.save(filename)

    def undo(self):
        if len(self.undolist) > 1:
            self.undolist.pop()
            self.gimg, self.bimg = self.undolist[-1]
            self.update(False)
            # if logger:
            #     self.logging("# Undo")
        else:
            # if logger:
            print("# Max undos reached")

    def update(self):
        self.master.geometry('%dx%d' % (self.gimg.size[0], self.gimg.size[1]))
        image1 = PIL.ImageTk.PhotoImage(self.gimg)
        self.label_image.configure(image=image1)
        self.label_image.image = image1
        self.master.wm_title(self.filename)

    def morph_helper(self, type_option):
        top = dialog_window(self.master)
        entry = Entry(top)
        entry.insert(END, "3")
        entry.grid(row=2, column=0)
        entry.focus_set()
        applyfn = lambda: self.morph(int(entry.get()), top, type_option)
        top.setapply(applyfn)

    def morph(self, count, top, morph_type):
        # Should change to non-square shape for nicer binary images
        img2 = PIL.Image.new(mode="1", size = self.gimg.size)
        # convertion to "L" was necessary for some reason
        if morph_type=="Erosion":
            tmp = scipy.ndimage.binary_erosion(self.gimg.convert("L"),
                    structure=morph_elemt(count))
        elif morph_type=="Dilation":
            tmp = scipy.ndimage.binary_dilation(self.gimg.convert("L"),
                    structure=morph_elemt(count))
        elif morph_type=="Opening":
            tmp = scipy.ndimage.binary_opening(self.gimg.convert("L"),
                    structure=morph_elemt(count))
        elif morph_type=="Closing":
            tmp = scipy.ndimage.binary_closing(self.gimg.convert("L"),
                    structure=morph_elemt(count))

        img2.putdata(255 * tmp.flatten())
        top.destroy()
        self.gimg = img2.convert("1")
        self.update()



root = Tk()
gui = Imagewindow(root)

