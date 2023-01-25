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
        self.label.grid(row = 0, column=1, pady=20)

        self.defaultImage = "WikiNoImage.png"

        self.prev_button = tk.Button(self, text="Previous", command=master.prev_page)
        self.prev_button.grid(row = 1, column = 0, padx = 30, pady=10)

        self.add_button = tk.Button(self, text="Add New Page", command=master.create_page)
        self.add_button.grid(row = 1, column = 1, padx = 30, pady=10)

        self.next_button = tk.Button(self, text="Next", command=master.next_page)
        self.next_button.grid(row = 1, column = 2, padx = 30, pady=10)
        
        row1 = pageRow()
        row1Array = row1.startRow(self)
        row1.generateRow(2, row1Array)

        row2 = pageRow()
        row2Array = row2.startRow(self)
        row2.generateRow(3, row2Array)

        row3 = pageRow()
        row3Array = row3.startRow(self)
        row3.generateRow(4, row3Array)

        row4 = pageRow()
        row4Array = row4.startRow(self)
        row4.generateRow(5, row4Array)

    def imageClick(self, event = None):
            print('clicked')

class pageRow:
    def __init__(self):
        self

    def startRow(self, master):
        self.image = Image.open(master.defaultImage)
        self.photo = ImageTk.PhotoImage(self.image)
        self.displayImage = tk.Label(master, image = self.photo)
        self.displayImage.bind('<Button-1>', master.imageClick)
        self.displayImageButton = tk.Button(master, image = self.photo, command = master.imageClick)

        self.text_box = tk.Text(master, height = 7, width = 52)
        return self.displayImage, self.displayImageButton, self.text_box
    
    def generateRow(self, rowNum, newWidget):
        newWidget[0].grid(row = rowNum, column = 0, padx = 60, pady=10)
        newWidget[1].grid(row = rowNum, column = 0, padx = 60, pady=10)
        newWidget[2].grid(row = rowNum, column = 1, padx = 60, pady=10)


if __name__ == '__main__':
    app = LeafletCreator()
    app.mainloop()