import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk

pageCounter = 1

class LeafletCreator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Leaflet Creator")
        self.geometry("1000x900")

        self.pages = []
        self.current_page = 0

        self.create_page()

    def create_page(self):
        global pageCounter
        self.pages.append(LeafletPage(self, pageCounter))
        pageCounter = pageCounter + 1
        self.show_page()

    def show_page(self):
        self.pages[self.current_page].grid()

    def next_page(self):
        self.pages[self.current_page].grid_forget()
        self.current_page = (self.current_page + 1) % len(self.pages)
        self.show_page()

    def prev_page(self):
        self.pages[self.current_page].grid_forget()
        self.current_page = (self.current_page - 1) % len(self.pages)
        self.show_page()

class LeafletPage(tk.Frame):
    def __init__(self, master, number):
        super().__init__(master)

        self.label = tk.Label(self, text="Page " + str(number))
        self.label.grid(row = 0, column=1, pady=20)

        self.prev_button = tk.Button(self, text="Previous", command=master.prev_page)
        self.prev_button.grid(row = 1, column = 0, padx = 30, pady=10)

        self.add_button = tk.Button(self, text="Add New Page", command=master.create_page)
        self.add_button.grid(row = 1, column = 1, padx = 30, pady=10)

        self.next_button = tk.Button(self, text="Next", command=master.next_page)
        self.next_button.grid(row = 1, column = 2, padx = 30, pady=10)
        
        self.row1 = pageRow(self, 2)
        self.row2 = pageRow(self, 3)
        self.row3 = pageRow(self, 4)
        self.row4 = pageRow(self, 5)

class pageRow:
    def __init__(self, master, rowNum):
        self.defaultImage = "WikiNoImage.png"
        self.image = Image.open(self.defaultImage)
        self.resizeImage = self.image.resize((150, 150))
        self.photo = ImageTk.PhotoImage(self.resizeImage)
        self.labelImage = tk.Label(master, image = self.photo)
        self.labelImage.image = self.photo
        self.labelImage.bind("<Button-1>", self.imageClick)
        self.theMaster = master
        
        self.text_box = tk.Text(master, height = 9, width = 52)

        self.labelImage.grid(row = rowNum, column = 0, padx = 60, pady=10)
        self.text_box.grid(row = rowNum, column = 1, padx = 60, pady=10)

    def imageClick(self, event = None):
        filetypes = (('image png', '*.png'), ('image jpg', '*.jpg'), ('All files', '*.*'))
        filename = fd.askopenfilename(title = 'Open Images', initialdir = '/', filetypes = filetypes)
        print(filename)
        self.image = Image.open(filename)
        self.resizeImage = self.image.resize((150, 150))
        self.photo = ImageTk.PhotoImage(self.resizeImage)
        self.labelImage.configure(image = self.photo)
        self.labelImage.image = self.photo
        self.defaultImage = filename

    def getRow(self):
        return self.labelImage, self.text_box


if __name__ == '__main__':
    app = LeafletCreator()
    app.mainloop()