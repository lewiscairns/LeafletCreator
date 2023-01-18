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
        self.pages[self.current_page].pack()

    def next_page(self):
        self.pages[self.current_page].pack_forget()
        self.current_page = (self.current_page + 1) % len(self.pages)
        self.show_page()

    def prev_page(self):
        self.pages[self.current_page].pack_forget()
        self.current_page = (self.current_page - 1) % len(self.pages)
        self.show_page()

class LeafletPage(tk.Frame):
    def __init__(self, master, number):
        super().__init__(master)

        self.label = tk.Label(self, text="Page " + str(number))
        self.label.pack()
        
        self.text_box_1 = tk.Text(self, height = 5, width = 52)
        self.text_box_1.pack()
        self.text_box_2 = tk.Text(self, height = 5, width = 52)
        self.text_box_2.pack()
        self.text_box_3 = tk.Text(self, height = 5, width = 52)
        self.text_box_3.pack()
        self.text_box_4 = tk.Text(self, height = 5, width = 52)
        self.text_box_4.pack()

        self.defaultImage = "WikiNoImage.png"

        self.image1 = Image.open(self.defaultImage)
        self.photo1 = ImageTk.PhotoImage(self.image1)
        self.displayImage1 = tk.Label(self, image = self.photo1)
        self.displayImage1.pack()
        self.displayImage1.bind('<Button-1>', self.imageClick)
        self.displayImageButton1 = tk.Button(self, image = self.photo1, command = self.imageClick)
        self.displayImage1.pack()
        self.displayImageButton1 = tk.Button(self, text = "Close", command = self.destroy)
        self.displayImage1.pack()

        self.next_button = tk.Button(self, text="Next", command=master.next_page)
        self.next_button.pack()

        self.prev_button = tk.Button(self, text="Previous", command=master.prev_page)
        self.prev_button.pack()

        self.add_button = tk.Button(self, text="Add New Page", command=master.create_page)
        self.add_button.pack()

    def imageClick(self, event = None):
        print('clicked')

if __name__ == '__main__':
    app = LeafletCreator()
    app.mainloop()