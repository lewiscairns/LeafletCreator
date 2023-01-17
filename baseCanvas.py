import tkinter as tk
from tkinter import ttk

pageCounter = 1

class LeafletCreator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Multiple Pages")
        self.geometry("800x600")

        self.pages = []
        self.current_page = 0

        self.create_page()

    def create_page(self):
        global pageCounter
        self.pages.append(BlankPage(self, pageCounter))
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

class BlankPage(tk.Frame):
    def __init__(self, master, number):
        super().__init__(master)

        self.label = tk.Label(self, text="This is a blank page " + str(number))
        self.label.pack()

        self.next_button = tk.Button(self, text="Next", command=master.next_page)
        self.next_button.pack()

        self.prev_button = tk.Button(self, text="Previous", command=master.prev_page)
        self.prev_button.pack()
        self.add_button = tk.Button(self, text="Add New Page", command=master.create_page)
        self.add_button.pack()

if __name__ == '__main__':
    app = LeafletCreator()
    app.mainloop()