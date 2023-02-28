import os
import sys

import fileIO
import menuBar
import sentenceAnalysis
import rightClickMenu

import tkinter as tk
from tkinter import filedialog as fd

import numpy as np
import re
from textblob import Word
from PIL import Image, ImageTk



class LeafletCreator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Untitled - Leaflet Creator")
        self.geometry("1000x900")

        self.pages = []
        self.current_page = 0
        self.page_counter = 0

        self.create_page()

        self.user_title = "Untitled"

        self.saved_folder = "C:\Leaflets"

        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.load)
        self.file_menu.add_command(label="Save", command=self.save)
        self.file_menu.add_command(label="Save As", command=self.save_as)
        self.file_menu.add_command(label="Change Title", command=self.title_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=self.destroy)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.page_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.page_menu.add_command(label="New Page", command=self.create_page)
        self.page_menu.add_command(label="Move Page", command=self.move_page)
        self.menu_bar.add_cascade(label="Page", menu=self.page_menu)

        self.generate_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.generate_menu.add_command(label="Generate", command=self.generate)
        self.menu_bar.add_cascade(label="Generate", menu=self.generate_menu)

        self.recommendation_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.recommendation_menu.add_command(label="Reading Level", command=self.change_reading_level)
        self.recommendation_menu.add_command(label="Word Count", command=self.change_word_count)
        self.recommendation_menu.add_command(label="Polarity", command=self.change_polarity)
        self.menu_bar.add_cascade(label="Recommendations", menu=self.recommendation_menu)

        self.font_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.font_menu.add_command(label="Font Style", command=self.change_font)
        self.font_menu.add_command(label="Font Size", command=self.change_font_size)
        self.menu_bar.add_cascade(label="Font", menu=self.font_menu)

        self.watermark_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.watermark_menu.add_command(label="Edit Watermark", command=self.edit_watermark)
        self.menu_bar.add_cascade(label="Watermark", menu=self.watermark_menu)

        self.reading_level = 90
        self.word_count = 10
        self.polarity = 0
        self.common_words = open('top-10000-words.txt', 'r').read().splitlines()
        self.ignore_uncommon_words = [""]
        self.font_style = "Times New Roman"
        self.font_size = 12
        self.watermark_image = "WikiWatermark.png"
        self.watermark_text = ""

        self.lift()

    def show_page(self):
        self.pages[self.current_page].grid()

    def new_file(self):
        menuBar.new_file(self)

    def title_file(self):
        menuBar.title_file(self, LeafletCreator)

    def create_page(self):
        menuBar.create_page(self, LeafletPage)

    def next_page(self):
        menuBar.next_page(self)

    def prev_page(self):
        menuBar.prev_page(self)

    def move_page(self):
        menuBar.move_page(self)

    def generate(self):
        menuBar.generate(self)

    def save_as(self):
        fileIO.save_as(self)

    def save(self):
        fileIO.save(self)

    def saving(self):
        fileIO.saving(self)

    def load(self):
        fileIO.load(self, LeafletCreator, LeafletPage)

    def change_reading_level(self):
        menuBar.ChangeReading(self)

    def change_word_count(self):
        menuBar.ChangeWordCount(self)

    def change_font(self):
        menuBar.ChangeFont(self)

    def change_font_size(self):
        menuBar.ChangeFontSize(self)

    def change_polarity(self):
        menuBar.ChangePolarity(self)

    def edit_watermark(self):
        menuBar.Watermark(self)

    @staticmethod
    def retrieve_input(text_box):
        input_value = text_box.get("1.0", "end-1c")
        return input_value


class LeafletPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.prev_button = tk.Button(self, text="Previous", command=master.prev_page, cursor="hand2")
        self.prev_button.grid(row=1, column=0, padx=30, pady=10)

        self.page_title = tk.Label(self, text="Page " + str(master.page_counter))
        self.page_title.grid(row=1, column=1, padx=30, pady=10)

        self.next_button = tk.Button(self, text="Next", command=master.next_page, cursor="hand2")
        self.next_button.grid(row=1, column=2, padx=30, pady=10)

        self.row1 = PageRow(self, 3, master)
        self.row2 = PageRow(self, 4, master)
        self.row3 = PageRow(self, 5, master)
        self.row4 = PageRow(self, 6, master)

    def add_row(self, label, text):
        image = Image.open(label)
        resize_image = image.resize((150, 150))
        photo = ImageTk.PhotoImage(resize_image)
        if self.row1.text_box.get("1.0", "end-1c") == "":
            self.row1.label_image.configure(image=photo)
            self.row1.label_image.image = photo
            self.row1.text_box.insert(tk.END, text)
        elif self.row2.text_box.get("1.0", "end-1c") == "":
            self.row2.label_image.configure(image=photo)
            self.row2.label_image.image = photo
            self.row2.text_box.insert(tk.END, text)
        elif self.row3.text_box.get("1.0", "end-1c") == "":
            self.row3.label_image.configure(image=photo)
            self.row3.label_image.image = photo
            self.row3.text_box.insert(tk.END, text)
        elif self.row4.text_box.get("1.0", "end-1c") == "":
            self.row4.label_image.configure(image=photo)
            self.row4.label_image.image = photo
            self.row4.text_box.insert(tk.END, text)
        else:
            print("Error: No more rows available")


class PageRow:
    def __init__(self, master, row_num, leaflet_master):
        self.leaflet_master = leaflet_master
        self.master = master
        self.row_num = row_num

        self.filename = "WikiNoImage.png"
        self.image = Image.open(self.filename)
        self.resize_image = self.image.resize((150, 150))
        self.photo = ImageTk.PhotoImage(self.resize_image)
        self.label_image = tk.Label(master, image=self.photo, cursor="hand2")
        self.label_image.image = self.photo
        self.label_image.bind("<Button-1>", self.image_click)

        self.text_box = tk.Text(master, height=9, width=52, wrap="word")
        self.text_box.tag_configure("wrong", foreground="red", underline=True)
        self.text_box.tag_configure("uncommon", foreground="blue", underline=True)
        self.text_box.bind("<KeyRelease>", self.check_spelling)
        self.text_box.bind("<space>", self.check_sentence)
        self.text_box.bind("<Button-3>", self.word_right_click)

        self.complexity_filename = "WikiGreenCircle.png"
        self.complexity_image = Image.open(self.complexity_filename)
        self.complexity_resize_image = self.complexity_image.resize((100, 100))
        self.complexity_photo = ImageTk.PhotoImage(self.complexity_resize_image)
        self.complexity_icon = tk.Label(master, image=self.complexity_photo, cursor="hand2")
        self.complexity_icon.image = self.complexity_photo

        self.label_image.grid(row=row_num, column=0, padx=60, pady=10)
        self.text_box.grid(row=row_num, column=1, padx=60, pady=10)
        self.complexity_icon.grid(row=row_num, column=2, padx=60, pady=10)

        self.regex = re.compile('[^a-zA-Z]')
        self.replacement_word = ""
        self.synonyms = []

        self.sentence_complexity = "Good"
        self.sentence_issues = np.array([False, False, False])
        self.reading_level = 0
        self.word_count = 0
        self.polarity = 0
        self.complexity_recommendations = ["", "", ""]
        self.complexity_icon.bind("<Button-1>", self.show_complexity_recommendations)
        self.misspelled_tag = []
        self.text = ""
        self.num_spaces = 0

    def get_row(self):
        return self.filename, self.text_box

    def image_click(self, event=None):
        filetypes = (('image png', '*.png'), ('image jpg', '*.jpg'), ('All files', '*.*'))
        self.filename = fd.askopenfilename(title='Open Images', initialdir='C:/Program Files/LeafletCreator/Images', filetypes=filetypes)
        self.image = Image.open(self.filename)
        self.resize_image = self.image.resize((150, 150))
        self.photo = ImageTk.PhotoImage(self.resize_image)
        self.label_image.configure(image=self.photo)
        self.label_image.image = self.photo

    def word_right_click(self, event):
        rightClickMenu.word_right_click(self, event)

    def check_sentence(self, event):
        sentenceAnalysis.check_sentence(self)

    def show_complexity_recommendations(self, event):
        sentenceAnalysis.show_complexity_recommendations(self)

    def replace_word(self):
        rightClickMenu.replace_word(self)

    def replace_synonym(self):
        rightClickMenu.replace_synonym(self)

    def copy_word(self):
        rightClickMenu.copy_word(self)

    def paste_word(self):
        rightClickMenu.paste_word(self)

    def check_spelling(self, event):
        rightClickMenu.check_spelling(self)


def new_file():
    os.execl(sys.executable, sys.executable, *sys.argv)


if __name__ == '__main__':
    app = LeafletCreator()
    app.mainloop()
