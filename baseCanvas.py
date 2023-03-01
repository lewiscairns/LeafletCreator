import os
import sys

import fileIO
import menuBar
import complexityAnalysis
import rightClickMenu

import tkinter as tk
from tkinter import filedialog as fd

import numpy as np
import re
from PIL import Image, ImageTk


class LeafletCreator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Untitled - Leaflet Creator")
        self.geometry("1000x900")

        self.pages = []
        self.current_page = 0
        self.page_counter = 0

        menuBar.create_page(self, LeafletPage)

        self.user_title = "Untitled"

        self.saved_folder = "C:/Leaflets"

        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.file_menu.add_command(label="New", command=lambda: menuBar.new_file(self))
        self.file_menu.add_command(label="Open", command=lambda: fileIO.load(self, LeafletCreator, LeafletPage))
        self.file_menu.add_command(label="Save", command=lambda: fileIO.save(self))
        self.file_menu.add_command(label="Save As", command=lambda: fileIO.save_as(self))
        self.file_menu.add_command(label="Change Title", command=lambda: menuBar.title_file(self, LeafletCreator))
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=self.destroy)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.page_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.page_menu.add_command(label="New Page", command=lambda: menuBar.create_page(self, LeafletPage))
        self.page_menu.add_command(label="Move Page", command=lambda: menuBar.move_page(self))
        self.menu_bar.add_cascade(label="Page", menu=self.page_menu)

        self.generate_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.generate_menu.add_command(label="Generate", command=lambda: menuBar.generate(self))
        self.menu_bar.add_cascade(label="Generate", menu=self.generate_menu)

        self.recommendation_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.recommendation_menu.add_command(label="Reading Level", command=lambda: menuBar.ChangeReading(self))
        self.recommendation_menu.add_command(label="Word Count", command=lambda: menuBar.ChangeWordCount(self))
        self.recommendation_menu.add_command(label="Sentiment Rating", command=lambda: menuBar.ChangeSentiment(self))
        self.menu_bar.add_cascade(label="Recommendations", menu=self.recommendation_menu)

        self.font_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.font_menu.add_command(label="Font Style", command=lambda: menuBar.ChangeFont(self))
        self.font_menu.add_command(label="Font Size", command=lambda: menuBar.ChangeFontSize(self))
        self.menu_bar.add_cascade(label="Font", menu=self.font_menu)

        self.watermark_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.watermark_menu.add_command(label="Edit Footer", command=lambda: menuBar.Footer(self))
        self.menu_bar.add_cascade(label="Footer", menu=self.watermark_menu)

        self.reading_level = 90
        self.word_count = 10
        self.polarity = 0
        self.common_words = open('top-10000-words.txt', 'r').read().splitlines()
        self.ignore_uncommon_words = [""]
        self.font_style = "Times New Roman"
        self.font_size = 18
        self.watermark_image = "images/WikiWatermark.png"
        self.watermark_text = "NHS 2022"

        self.lift()

    def show_page(self):
        self.pages[self.current_page].grid()

    @staticmethod
    def retrieve_input(text_box):
        input_value = text_box.get("1.0", "end-1c")
        return input_value


class LeafletPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.prev_button = tk.Button(self, text="Previous", command=lambda: menuBar.next_page(self), cursor="hand2")
        self.prev_button.grid(row=1, column=0, padx=30, pady=10)

        self.page_title = tk.Label(self, text="Page " + str(master.page_counter))
        self.page_title.grid(row=1, column=1, padx=30, pady=10)

        self.next_button = tk.Button(self, text="Next", command=lambda: menuBar.prev_page(master), cursor="hand2")
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


# noinspection PyUnusedLocal
class PageRow:
    def __init__(self, master, row_num, leaflet_master):
        self.leaflet_master = leaflet_master
        self.master = master
        self.row_num = row_num

        self.filename = "images/WikiNoImage.png"
        self.image = Image.open(self.filename)
        self.resize_image = self.image.resize((150, 150))
        self.photo = ImageTk.PhotoImage(self.resize_image)
        self.label_image = tk.Label(master, image=self.photo, cursor="hand2")
        self.label_image.image = self.photo
        self.label_image.bind("<Button-1>", self.image_click)

        self.text_box = tk.Text(master, height=9, width=52, wrap="word")
        self.text_box.tag_configure("wrong", foreground="red", underline=True)
        self.text_box.tag_configure("uncommon", foreground="blue", underline=True)
        self.text_box.bind("<KeyRelease>", lambda event: rightClickMenu.check_spelling(self))
        self.text_box.bind("<space>", lambda event: complexityAnalysis.check_sentence(self))
        self.text_box.bind("<Button-3>", lambda event: rightClickMenu.word_right_click(self, event))

        self.complexity_filename = "images/WikiGreenCircle.png"
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
        self.complexity_icon.bind("<Button-1>", lambda event: complexityAnalysis.show_complexity_recommendations(self))
        self.misspelled_tag = []
        self.text = ""
        self.num_spaces = 0

    def get_row(self):
        return self.filename, self.text_box

    def image_click(self, event=None):
        filetypes = (('image png', '*.png'), ('image jpg', '*.jpg'), ('All files', '*.*'))
        self.filename = fd.askopenfilename(title='Open Images', initialdir='C:/Program Files/LeafletCreator/Images',
                                           filetypes=filetypes)
        self.image = Image.open(self.filename)
        self.resize_image = self.image.resize((150, 150))
        self.photo = ImageTk.PhotoImage(self.resize_image)
        self.label_image.configure(image=self.photo)
        self.label_image.image = self.photo


def new_file():
    os.execl(sys.executable, sys.executable, *sys.argv)


if __name__ == '__main__':
    app = LeafletCreator()
    app.mainloop()
