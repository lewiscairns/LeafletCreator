import os
import sys
import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter.simpledialog import askstring

import numpy as np
import textstat
import re
from textblob import Word
from PIL import Image, ImageTk
import docxFiles
import pickle as lc
from nltk.corpus import wordnet
import subprocess

pageCounter = 1


class LeafletCreator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Untitled - Leaflet Creator")
        self.geometry("1000x900")

        self.pages = []
        self.current_page = 0

        self.create_page()

        self.user_title = "Untitled"

        self.saved_folder = "C:\Leaflets"

        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.file_menu.add_command(label="New", command=new_file)
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
        self.menu_bar.add_cascade(label="Recommendations", menu=self.recommendation_menu)

        self.font_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.font_menu.add_command(label="Font Style", command=self.change_font)
        self.font_menu.add_command(label="Font Size", command=self.change_font_size)
        self.menu_bar.add_cascade(label="Font", menu=self.font_menu)

        self.reading_level = 90
        self.word_count = 10
        self.common_words = open('top-10000-words.txt', 'r').read().splitlines()
        self.ignore_uncommon_words = [""]
        self.font_style = "Times New Roman"
        self.font_size = 12

        self.lift()

    def title_file(self):
        self.user_title = tk.simpledialog.askstring("File Name", "Please enter a title for this file")
        new_title = self.user_title + " - Leaflet Creator"
        LeafletCreator.title(self, new_title)

    def create_page(self):
        global pageCounter
        self.pages.append(LeafletPage(self))
        pageCounter = pageCounter + 1
        if len(self.pages) > 1:
            self.pages[self.current_page].grid_forget()
            self.current_page = len(self.pages) - 1
            self.show_page()
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
        folder_selected = fd.askdirectory(title="Select Folder To Generate File")
        all_rows = []
        page_counter = 0
        for page in self.pages:
            all_rows.append([page_counter])
            for row in page.row1, page.row2, page.row3, page.row4:
                label, text = row.get_row()
                all_rows[page_counter].append([label, self.retrieve_input(text)])
            page_counter = page_counter + 1
        docxFiles.create_document(self.user_title, all_rows, folder_selected, self.font_style, self.font_size)
        tk.messagebox.showinfo("Success", "Your document has been created, please open it in Word")

    def move_page(self):
        print("Move Page")

    def save_as(self):
        try:
            self.saved_folder = fd.askdirectory(title="Select Folder To Generate File")
            self.saving()
            tk.messagebox.showinfo("Success", "Your document has been saved")
        except Exception as e:
            print("Error: " + str(e))

    def save(self):
        try:
            self.saving()
        except Exception as e:
            print("Error: " + str(e))

    def saving(self):
        with open(self.saved_folder + "/" + self.user_title + ".lc", "wb") as file:
            pages_text = []
            for page in self.pages:
                page_text = []
                for row in page.row1, page.row2, page.row3, page.row4:
                    label, text = row.get_row()
                    page_text.append([label, self.retrieve_input(text)])
                pages_text.append(page_text)
            data = [self.user_title, self.font_size, self.font_style, self.word_count, self.reading_level, self.ignore_uncommon_words, pages_text]
            lc.dump(data, file, protocol=lc.HIGHEST_PROTOCOL)

    def load(self):
        self.pages[self.current_page].grid_forget()
        filetypes = (('leaflet.lc', '*.lc'), ('All files', '*.*'))
        filename = fd.askopenfilename(title='Open Leaflet', initialdir='/', filetypes=filetypes)
        try:
            with open(filename, "rb") as file:
                data = lc.load(file)
                self.user_title = data[0]
                self.font_size = data[1]
                self.font_style = data[2]
                self.word_count = data[3]
                self.reading_level = data[4]
                self.ignore_uncommon_words = data[5]
                new_title = (self.user_title + " - Leaflet Creator")
                LeafletCreator.title(self, new_title)
                self.pages = []
                for page in data[6]:
                    self.pages.append(LeafletPage(self))
                    for row in page:
                        self.pages[-1].add_row(row[0], row[1])
        except Exception as e:
            print("Error: " + str(e))
        self.current_page = 0
        self.show_page()

    def change_reading_level(self):
        ChangeReading(self)

    def change_word_count(self):
        ChangeWordCount(self)

    def change_font(self):
        ChangeFont(self)

    def change_font_size(self):
        ChangeFontSize(self)

    @staticmethod
    def retrieve_input(text_box):
        input_value = text_box.get("1.0", "end-1c")
        return input_value


class ChangeFont:
    def __init__(self, master):
        self.master = master
        self.top = tk.Toplevel(master)
        self.top.geometry("300x150")
        self.top.title("Font Style")
        self.arial_button = tk.Button(self.top, text="Arial", command=self.arial)
        self.times_button = tk.Button(self.top, text="Times New Roman", command=self.times)
        self.arial_button.pack()
        self.times_button.pack()

    def arial(self):
        self.master.font_style = "Arial"
        self.top.destroy()
        tk.messagebox.showinfo("Success", "Your document will now generate in Arial as the font style")

    def times(self):
        self.master.font_style = "Times New Roman"
        self.top.destroy()
        tk.messagebox.showinfo("Success", "Your document will now generate in Times New Roman as the font style")


class ChangeFontSize:
    def __init__(self, master):
        self.master = master
        self.top = tk.Toplevel(master)
        self.top.geometry("300x150")
        self.top.title("Font Size")
        self.top_label = tk.Label(self.top, text="Recommended Font Size is 16")
        self.top_button_up = tk.Button(self.top, text="+", command=self.increase_font_size)
        self.top_button_down = tk.Button(self.top, text="-", command=self.decrease_font_size)
        self.top_font_size = tk.IntVar()
        self.top_font_size.set(self.master.font_size)
        self.top_entry = tk.Entry(self.top, textvariable=self.top_font_size)
        self.top_entry.configure(state="readonly")
        self.top_button = tk.Button(self.top, text="Close", command=self.top.destroy)
        self.top_label.grid(row=0, column=0, columnspan=2)
        self.top_button_up.grid(row=1, column=0)
        self.top_entry.grid(row=1, column=1)
        self.top_button_down.grid(row=1, column=2)
        self.top_button.grid(row=2, column=0, columnspan=2)

    def increase_font_size(self):
        self.master.font_size = self.master.font_size + 1
        self.top_font_size.set(self.master.font_size)

    def decrease_font_size(self):
        self.master.font_size = self.master.font_size - 1
        self.top_font_size.set(self.master.font_size)


class ChangeReading:
    def __init__(self, master):
        self.master = master
        self.top = tk.Toplevel(master)
        self.top.geometry("300x150")
        self.top.title("Reading Level")
        self.top_label = tk.Label(self.top, text="Recommended Reading Level is 90")
        self.top_button_up = tk.Button(self.top, text="+", command=self.increase_reading_level)
        self.top_button_down = tk.Button(self.top, text="-", command=self.decrease_reading_level)
        self.top_reading_level = tk.IntVar()
        self.top_reading_level.set(self.master.reading_level)
        self.top_entry = tk.Entry(self.top, textvariable=self.top_reading_level)
        self.top_entry.configure(state="readonly")
        self.top_button = tk.Button(self.top, text="Close", command=self.top.destroy)
        self.top_label.grid(row=0, column=0, columnspan=2)
        self.top_button_up.grid(row=1, column=0)
        self.top_entry.grid(row=1, column=1)
        self.top_button_down.grid(row=1, column=2)
        self.top_button.grid(row=2, column=0, columnspan=2)

    def increase_reading_level(self):
        self.master.reading_level = self.master.reading_level + 1
        self.top_reading_level.set(self.master.reading_level)

    def decrease_reading_level(self):
        self.master.reading_level = self.master.reading_level - 1
        self.top_reading_level.set(self.master.reading_level)


class ChangeWordCount:
    def __init__(self, master):
        self.master = master
        self.top = tk.Toplevel(master)
        self.top.geometry("300x150")
        self.top.title("Word Count")
        self.top_label = tk.Label(self.top, text="Recommended Word Count is 10")
        self.top_button_up = tk.Button(self.top, text="+", command=self.increase_word_count)
        self.top_button_down = tk.Button(self.top, text="-", command=self.decrease_word_count)
        self.top_word_count = tk.IntVar()
        self.top_word_count.set(self.master.word_count)
        self.top_entry = tk.Entry(self.top, textvariable=self.top_word_count)
        self.top_entry.configure(state="readonly")
        self.top_button = tk.Button(self.top, text="Close", command=self.top.destroy)
        self.top_label.grid(row=0, column=0, columnspan=2)
        self.top_button_up.grid(row=1, column=0)
        self.top_entry.grid(row=1, column=1)
        self.top_button_down.grid(row=1, column=2)
        self.top_button.grid(row=2, column=0, columnspan=2)

    def increase_word_count(self):
        self.master.word_count = self.master.word_count + 1
        self.top_word_count.set(self.master.word_count)

    def decrease_word_count(self):
        self.master.word_count = self.master.word_count - 1
        self.top_word_count.set(self.master.word_count)


class LeafletPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.prev_button = tk.Button(self, text="Previous", command=master.prev_page)
        self.prev_button.grid(row=1, column=0, padx=30, pady=10)

        self.page_title = tk.Label(self, text="Page " + str(pageCounter))
        self.page_title.grid(row=1, column=1, padx=30, pady=10)

        self.next_button = tk.Button(self, text="Next", command=master.next_page)
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
        self.label_image = tk.Label(master, image=self.photo)
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
        self.complexity_icon = tk.Label(master, image=self.complexity_photo)
        self.complexity_icon.image = self.complexity_photo

        self.label_image.grid(row=row_num, column=0, padx=60, pady=10)
        self.text_box.grid(row=row_num, column=1, padx=60, pady=10)
        self.complexity_icon.grid(row=row_num, column=2, padx=60, pady=10)

        self.regex = re.compile('[^a-zA-Z]')
        self.replacement_word = ""
        self.synonyms = []

        self.sentence_complexity = "Good"
        self.sentence_issues = np.array([False, False])
        self.reading_level = 0
        self.word_count = 0
        self.complexity_recommendations = ["", ""]
        self.complexity_icon.bind("<Button-1>", self.show_complexity_recommendations)
        self.misspelled_tag = []
        self.text = ""

        self.num_spaces = 0

    def show_complexity_recommendations(self, event):
        recommendation_text = ""
        for recommendation in self.complexity_recommendations:
            if recommendation != "":
                recommendation_text += "\n" + recommendation
        if recommendation_text == "":
            recommendation_text = "No recommendations available"
        top = tk.Toplevel(self.master)
        top.geometry("300x150")
        top.title("Recommendations")
        top_label = tk.Label(top, text=recommendation_text)
        top_button = tk.Button(top, text="Close", command=top.destroy)
        top_label.pack()
        top_button.pack()

    def check_sentence(self, event):
        self.reading_level = textstat.flesch_reading_ease(self.text_box.get("1.0", "end-1c"))
        if self.reading_level < self.leaflet_master.reading_level:
            self.sentence_issues[0] = True
            self.complexity_recommendations[0] = "Reading level is: " + str(
                round(self.reading_level)) + "\nTry keep it below " + str(self.leaflet_master.reading_level) + ".\n"
        elif self.reading_level > self.leaflet_master.reading_level:
            self.sentence_issues[0] = False
            self.complexity_recommendations[0] = ""

        self.word_count = len(self.text_box.get("1.0", "end-1c").split())
        if self.word_count > self.leaflet_master.word_count:
            self.sentence_issues[1] = True
            self.complexity_recommendations[1] = "Current word count is: " + str(
                self.word_count) + "\nTry keep it below " + str(self.leaflet_master.word_count) + " words.\n"
        elif self.word_count < self.leaflet_master.word_count:
            self.sentence_issues[1] = False
            self.complexity_recommendations[1] = ""
        self.update_complexity()

    def update_complexity(self):
        if np.count_nonzero(self.sentence_issues) > 1:
            self.sentence_complexity = "Bad"
        elif np.count_nonzero(self.sentence_issues) > 0:
            self.sentence_complexity = "Average"
        else:
            self.sentence_complexity = "Good"
        self.update_complexity_image()

    def update_complexity_image(self):
        if self.sentence_complexity == "Good":
            self.complexity_filename = "WikiGreenCircle.png"
        elif self.sentence_complexity == "Average":
            self.complexity_filename = "WikiYellowCircle.png"
        else:
            self.complexity_filename = "WikiRedCircle.png"

        self.complexity_image = Image.open(self.complexity_filename)
        self.complexity_resize_image = self.complexity_image.resize((100, 100))
        self.complexity_photo = ImageTk.PhotoImage(self.complexity_resize_image)
        self.complexity_icon.configure(image=self.complexity_photo)
        self.complexity_icon.image = self.complexity_photo

    def image_click(self, event=None):
        filetypes = (('image png', '*.png'), ('image jpg', '*.jpg'), ('All files', '*.*'))
        self.filename = fd.askopenfilename(title='Open Images', initialdir='C:/Program Files/LeafletCreator/Images', filetypes=filetypes)
        self.image = Image.open(self.filename)
        self.resize_image = self.image.resize((150, 150))
        self.photo = ImageTk.PhotoImage(self.resize_image)
        self.label_image.configure(image=self.photo)
        self.label_image.image = self.photo

    def get_row(self):
        return self.filename, self.text_box

    def word_complexity_check(self):
        for word in self.text.split(' '):
            word_positions = [i for i in range(len(self.text)) if self.text.startswith(word, i)]
            word = self.regex.sub('', word)
            for position in word_positions:
                if word in self.leaflet_master.common_words or word in self.leaflet_master.ignore_uncommon_words:
                    self.text_box.tag_remove("uncommon", f'1.{position}', f'1.{position + len(word)}')
                elif position in self.misspelled_tag:
                    self.text_box.tag_remove("uncommon", f'1.{position}', f'1.{position + len(word)}')
                else:
                    self.text_box.tag_add("uncommon", f'1.{position}', f'1.{position + len(word)}')

    def word_right_click(self, event):
        word = self.text_box.get("@%d,%d wordstart" % (event.x, event.y), "@%d,%d wordend" % (event.x, event.y))
        self.text_box.mark_set("insert", "@%d,%d" % (event.x, event.y))
        self.text_box.mark_set("sel.first", "insert wordstart")
        self.text_box.mark_set("sel.last", "insert wordend")
        word_menu = tk.Menu(self.master, tearoff=0)
        word_menu.add_command(label="Copy", command=self.copy_word)
        word_menu.add_command(label="Paste", command=self.paste_word)
        is_wrong = self.get_word_replacement(word)
        is_uncommon = self.get_word_synonym(word)
        if is_wrong:
            word_menu.add_separator()
            word_menu.add_command(label=self.replacement_word, command=self.replace_word)
        elif is_uncommon:
            word_menu.add_separator()
            word_menu.add_command(label=self.synonyms[1], command=self.replace_synonym)
            word_menu.add_separator()
            word_menu.add_command(label="ignore", command=self.leaflet_master.ignore_uncommon_words.append(word))
        word_menu.tk_popup(event.x_root, event.y_root, 0)

    def get_word_replacement(self, word):
        text = Word(word)
        suggestion = text.spellcheck()
        suggestion_text = suggestion[0]
        suggestion_text = str(suggestion_text).split(" ", 1)[0]
        suggestion_text = self.regex.sub('', suggestion_text)
        if suggestion_text == "n":
            return False
        elif suggestion_text != word:
            self.replacement_word = suggestion_text
            return True
        else:
            return False

    def get_word_synonym(self, word):
        if word in self.leaflet_master.common_words or word in self.leaflet_master.ignore_uncommon_words:
            return False
        else:
            for syn in wordnet.synsets(word):
                for lemma in syn.lemmas():
                    self.synonyms.append(lemma.name())
            return True

    def copy_word(self):
        self.text_box.clipboard_clear()
        self.text_box.clipboard_append(self.text_box.selection_get())

    def paste_word(self):
        self.text_box.insert(tk.INSERT, self.text_box.clipboard_get())

    def replace_word(self):
        self.text_box.delete("sel.first", "sel.last")
        self.text_box.insert("sel.first", self.replacement_word)
        self.word_complexity_check()

    def replace_synonym(self):
        self.text_box.delete("sel.first", "sel.last")
        self.text_box.insert("sel.first", self.synonyms[1])
        self.leaflet_master.ignore_uncommon_words.append(self.synonyms[1])

    def check_spelling(self, event):
        self.text = self.text_box.get("1.0", tk.END)
        current_spaces = self.text.count(' ')
        self.misspelled_tag = []
        if current_spaces != self.num_spaces:
            self.num_spaces = current_spaces
            for word in self.text.split(' '):
                word_positions = [i for i in range(len(self.text)) if self.text.startswith(word, i)]
                suggestion = Word.spellcheck(Word(word))
                suggestion_text = suggestion[0]
                suggestion_text = str(suggestion_text).split(" ", 1)[0]
                suggestion_text = self.regex.sub('', suggestion_text)
                word = self.regex.sub('', word)
                for position in word_positions:
                    self.misspelled_tag.append(position)
                    if suggestion_text != word and suggestion_text != "n":
                        self.text_box.tag_add("wrong", f'1.{position}', f'1.{position + len(word)}')
                    else:
                        self.text_box.tag_remove("wrong", f'1.{position}', f'1.{position + len(word)}')
                        self.misspelled_tag.remove(position)
            self.word_complexity_check()


def new_file():
    os.execl(sys.executable, sys.executable, *sys.argv)


if __name__ == '__main__':
    app = LeafletCreator()
    app.mainloop()
