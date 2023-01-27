import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
import docxFiles

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

    def generate(self):
        allRows = [[]]
        pageCounter = 0
        for page in self.pages:
            allRows.append([pageCounter])
            for row in page.row1, page.row2, page.row3, page.row4:
                label, text = row.getRow()
                allRows[pageCounter].append([label, self.retrieveInput(text)])
            pageCounter = pageCounter + 1
        allRows.pop(1)
        docxFiles.createDocument("Lets go running", allRows)
        tk.messagebox.showinfo("Success", "Your document has been created, please open it in Word")
 
    def retrieveInput(self, textBox):
        inputValue = textBox.get("1.0","end-1c")
        return inputValue

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

        self.generate_button = tk.Button(self, text="Generate", command=master.generate)
        self.generate_button.grid(row = 1, column = 3, padx = 30, pady=10)
        
        self.row1 = pageRow(self, 2)
        self.row2 = pageRow(self, 3)
        self.row3 = pageRow(self, 4)
        self.row4 = pageRow(self, 5)

class pageRow:
    def __init__(self, master, rowNum):
        self.filename = "WikiNoImage.png"
        self.image = Image.open(self.filename)
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
        self.filename = fd.askopenfilename(title = 'Open Images', initialdir = '/', filetypes = filetypes)
        print(self.filename)
        self.image = Image.open(self.filename)
        self.resizeImage = self.image.resize((150, 150))
        self.photo = ImageTk.PhotoImage(self.resizeImage)
        self.labelImage.configure(image = self.photo)
        self.labelImage.image = self.photo
        self.defaultImage = self.filename

    def getRow(self):
        return self.filename, self.text_box


if __name__ == '__main__':
    app = LeafletCreator()
    app.mainloop()