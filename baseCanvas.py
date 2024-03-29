# Import necessary libraries and modules
import os
import sys

import fileIO
import menuBar
import complexityAnalysis
import rightClickMenu

#import customtkinter as ct
import tkinter as tk
from tkinter import filedialog as fd

import numpy as np
import re
from PIL import Image, ImageTk

#This is the main class that holds all the leaflet information and is the main window of the program.
class LeafletCreator(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.title("Untitled - Leaflet Creator")
        self.state('zoomed')
        self.grid_columnconfigure(0, weight=1)

        # Set up the main window's variables
        self.pages = []
        self.current_page = 0
        self.page_counter = 0

        menuBar.create_page(self, LeafletPage)

        self.user_title = "Untitled"

        self.saved_folder = ""

        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        #Set up the menu bar and alls it's sub menus
        self.file_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.file_menu.add_command(label="New", command=lambda: new_file())
        self.file_menu.add_command(label="Open", command=lambda: fileIO.load(self, LeafletCreator, LeafletPage))
        self.file_menu.add_command(label="Save", command=lambda: fileIO.save(self))
        self.file_menu.add_command(label="Save As", command=lambda: fileIO.save_as(self))
        self.file_menu.add_command(label="Change Title", command=lambda: menuBar.title_file(self, LeafletCreator))
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=self.destroy)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.page_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.page_menu.add_command(label="New Page", command=lambda: menuBar.create_page(self, LeafletPage))
        self.menu_bar.add_cascade(label="Page", menu=self.page_menu)

        self.document_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.document_menu.add_command(label="Generate", command=lambda: menuBar.generate(self))
        self.document_menu.add_command(label="Edit Footer", command=lambda: menuBar.Footer(self))
        self.document_menu.add_separator()
        self.document_menu.add_command(label="Document Font Style", command=lambda: menuBar.ChangeFont(self))
        self.document_menu.add_command(label="Document Font Size", command=lambda: menuBar.ChangeFontSize(self))
        self.menu_bar.add_cascade(label="Document", menu=self.document_menu)

        self.settings_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.settings_menu.add_command(label="Reading Level", command=lambda: menuBar.ChangeReading(self))
        self.settings_menu.add_command(label="Word Count", command=lambda: menuBar.ChangeWordCount(self))
        self.settings_menu.add_command(label="Sentiment Rating", command=lambda: menuBar.ChangeSentiment(self))
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)

        self.easy_read_advice = tk.Menu(self.menu_bar, tearoff=False)
        self.easy_read_advice.add_command(label="What is Easy Read", command=lambda: menuBar.WhatEasyRead(self))
        self.easy_read_advice.add_command(label="English into Easy Read", command=lambda: menuBar.EnglishEasyRead(self))
        self.easy_read_advice.add_command(label="Style of Easy Read content", command=lambda: menuBar.ContentEasyRead(self))
        self.easy_read_advice.add_command(label="Do's and Don'ts", command=lambda: menuBar.DoEasyRead(self))
        self.menu_bar.add_cascade(label="Easy Read Information", menu=self.easy_read_advice)

        # Set up the document's settings
        self.reading_level = 90
        self.word_count = 15
        self.polarity = 0
        self.common_words = open('top-10000-words.txt', 'r').read().splitlines()
        self.ignore_words = []
        self.font_style = "Arial"
        self.font_size = 18
        self.watermark_image = "images/WikiWatermark.png"
        self.watermark_text = ""
        self.complex_grammar_list = ["might", "would", "should", "negatives", "if", "then", "while", "because", "why", "since", "although", "though", "so", "before", "after", "until", "whether", "when"]

        self.lift()

    # Function to change the current page
    def show_page(self):
        self.pages[self.current_page].grid()

    # Function to hide the current page
    @staticmethod
    def retrieve_input(text_box):
        input_value = text_box.get("1.0", "end-1c")
        return input_value

# This is the class for each page of the leaflet
class LeafletPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Set up the page's elements
        self.prev_button = tk.Button(self, text="Previous", font=("Arial", 14, "bold"), command=lambda: menuBar.prev_page(master))
        #self.prev_button = ct.CTkButton(self, fg_color="white", hover_color="lightgray", text_color="black", font=("Arial", 14, "bold"), text="Previous", command=lambda: menuBar.next_page(master), cursor="hand2")
        self.prev_button.grid(row=1, column=0, padx=30, pady=10)

        self.page_title = tk.Label(self, text="Page " + str(master.page_counter))
        self.page_title.configure(font=("Arial", 16, "bold"))
        self.page_title.grid(row=1, column=1, padx=30, pady=10)

        self.next_button = tk.Button(self, text="Next", font=("Arial", 14, "bold"), command=lambda: menuBar.next_page(master))
        #self.next_button = ct.CTkButton(self, fg_color="white", hover_color="lightgray", text_color="black", font=("Arial", 14, "bold"), text="Next", command=lambda: menuBar.prev_page(master), cursor="hand2")
        self.next_button.grid(row=1, column=2, padx=30, pady=10)

        # Set up the page's rows
        self.row1 = PageRow(self, 3, master)
        self.row2 = PageRow(self, 4, master)
        self.row3 = PageRow(self, 5, master)
        self.row4 = PageRow(self, 6, master)

    # Function to add a row to the page
    def add_row(self, label, text):
        # Open the image and resize it
        image = Image.open(label)
        resize_image = image.resize((148, 148))
        photo = ImageTk.PhotoImage(resize_image)
        # Check if the row is empty
        if not self.row1.built:
            # Add the image and text to the row
            self.row1.label_image.configure(image=photo)
            self.row1.label_image.image = photo
            self.row1.text_box.insert(tk.END, text)
            self.row1.filename = label
            self.row1.built = True
        elif not self.row2.built:
            self.row2.label_image.configure(image=photo)
            self.row2.label_image.image = photo
            self.row2.text_box.insert(tk.END, text)
            self.row2.filename = label
            self.row2.built = True
        elif not self.row3.built:
            self.row3.label_image.configure(image=photo)
            self.row3.label_image.image = photo
            self.row3.text_box.insert(tk.END, text)
            self.row3.filename = label
            self.row3.built = True
        elif not self.row4.built:
            self.row4.label_image.configure(image=photo)
            self.row4.label_image.image = photo
            self.row4.text_box.insert(tk.END, text)
            self.row4.filename = label
            self.row4.built = True
        else:
            print("Error: No more rows available")


# noinspection PyUnusedLocal
# This is the class for each row of the leaflet
class PageRow:
    def __init__(self, master, row_num, leaflet_master):

        # Set up the row's class related variables
        self.built = False
        self.leaflet_master = leaflet_master
        self.master = master
        self.row_num = row_num

        # Set up the row's image variables
        self.filename = "images/WikiNoImage.png"
        self.image = Image.open(self.filename)
        self.resize_image = self.image.resize((148, 148))
        self.photo = ImageTk.PhotoImage(self.resize_image)
        self.label_image = tk.Label(master, image=self.photo, cursor="hand2")
        self.label_image.image = self.photo
        self.label_image.bind("<Button-1>", self.image_click)

        # Set up the row's text box
        self.text_box = tk.Text(master, height=6, width=30, wrap="word")
        self.text_box.configure(font=("Arial", 16))
        self.text_box.tag_configure("wrong", foreground="red", underline=True)
        self.text_box.tag_configure("uncommon", foreground="blue", underline=True)
        self.text_box.tag_configure("bold", font=("Arial", 16, "bold"))
        self.text_box.bind("<KeyRelease>", lambda event: rightClickMenu.check_spelling(self))
        self.text_box.bind("<Key>", lambda event: complexityAnalysis.check_sentence(self))
        self.text_box.bind("<Button-3>", lambda event: rightClickMenu.word_right_click(self, event))

        # Set up the row's complexity image
        self.complexity_filename = "images/WikiGreenCircle.png"
        self.complexity_image = Image.open(self.complexity_filename)
        self.complexity_resize_image = self.complexity_image.resize((100, 100))
        self.complexity_photo = ImageTk.PhotoImage(self.complexity_resize_image)
        self.complexity_icon = tk.Label(master, image=self.complexity_photo, cursor="hand2")
        self.complexity_icon.image = self.complexity_photo

        # Set up the row's grid
        self.label_image.grid(row=row_num, column=0, padx=60, pady=10)
        self.text_box.grid(row=row_num, column=1, padx=60, pady=10)
        self.complexity_icon.grid(row=row_num, column=2, padx=60, pady=10)

        # Set up the row's variables
        self.regex = re.compile('[^a-zA-Z]')
        self.replacement_word = ""
        self.synonyms = []

        self.sentence_complexity = "Good"
        self.sentence_issues = np.array([False, False, False, False])
        self.reading_level = 0
        self.word_count = 0
        self.polarity = 0
        self.complexity_recommendations = []
        self.complexity_icon.bind("<Button-1>", lambda event: complexityAnalysis.show_complexity_recommendations(self))
        self.misspelled_tag = []
        self.text = ""
        self.num_spaces = 0

    # Function to get the row's variables
    def get_row(self):
        return self.filename, self.text_box

    # Function to change the row's image
    def image_click(self, event=None):
        filetypes = (('image png', '*.png'), ('image jpg', '*.jpg'), ('All files', '*.*'))
        self.filename = fd.askopenfilename(title='Open Images', initialdir='C:/Program Files/LeafletCreator/Images',
                                           filetypes=filetypes)
        self.image = Image.open(self.filename)
        self.resize_image = self.image.resize((148, 148))
        self.photo = ImageTk.PhotoImage(self.resize_image)
        self.label_image.configure(image=self.photo)
        self.label_image.image = self.photo

# start a new version of the program if new file is selected
def new_file():
    os.execl(sys.executable, sys.executable, *sys.argv)

# Function to create the UI for the program
if __name__ == '__main__':
    app = LeafletCreator()
    app.mainloop()
