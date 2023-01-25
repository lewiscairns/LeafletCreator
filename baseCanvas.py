import tkinter as tk
from PIL import Image, ImageTk

pageCounter = 1

class LeafletCreator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Leaflet Creator")
        self.geometry("900x800")

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
        self.label.grid()

        self.defaultImage = "WikiNoImage.png"

        self.prev_button = tk.Button(self, text="Previous", command=master.prev_page)
        self.prev_button.grid(row = 0, column = 0, padx = 30, pady=10)

        self.add_button = tk.Button(self, text="Add New Page", command=master.create_page)
        self.add_button.grid(row = 0, column = 1, padx = 30, pady=10)

        self.next_button = tk.Button(self, text="Next", command=master.next_page)
        self.next_button.grid(row = 0, column = 2, padx = 30, pady=10)
        
        pageRow(self, 1)
        pageRow(self, 2)
        pageRow(self, 3)
        pageRow(self, 4)

    def imageClick(self, event = None):
            print('clicked')

class pageRow:
    def __init__(self, master, rowNum):
        self.image = Image.open(master.defaultImage)
        self.photo = ImageTk.PhotoImage(self.image)
        self.displayImage = tk.Label(master, image = self.photo)
        self.displayImage.grid(row = rowNum, column = 0, padx = 60, pady=10)
        self.displayImage.bind('<Button-1>', master.imageClick)
        self.displayImageButton = tk.Button(master, image = self.photo, command = master.imageClick)
        self.displayImage.grid(row = rowNum, column = 0, padx = 60, pady=10)
        self.displayImageButton2 = tk.Button(master, text = "Close", command = master.destroy)
        self.displayImage.grid(row = rowNum, column = 0, padx = 60, pady=10)

        self.text_box = tk.Text(master, height = 7, width = 52)
        self.text_box.grid(row = rowNum, column = 1, padx = 60, pady=10)


if __name__ == '__main__':
    app = LeafletCreator()
    app.mainloop()