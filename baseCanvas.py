import os
import sys
import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter.simpledialog import askstring

import textstat
import re
from textblob import Word
from PIL import Image, ImageTk
import docxFiles
import pickle as lc

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
                print(all_rows)
            page_counter = page_counter + 1
        docxFiles.create_document(self.user_title, all_rows, folder_selected)
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
            data = [self.user_title, pages_text]
            lc.dump(data, file, protocol=lc.HIGHEST_PROTOCOL)

    def load(self):
        self.pages[self.current_page].grid_forget()
        filetypes = (('leaflet.lc', '*.lc'), ('All files', '*.*'))
        filename = fd.askopenfilename(title='Open Leaflet', initialdir='/', filetypes=filetypes)
        try:
            with open(filename, "rb") as file:
                data = lc.load(file)
                self.user_title = data[0]
                self.title = (self.user_title + " - Leaflet Creator")
                self.pages = []
                for page in data[1]:
                    self.pages.append(LeafletPage(self))
                    for row in page:
                        self.pages[-1].add_row(row[0], row[1])
        except Exception as e:
            print("Error: " + str(e))
        self.current_page = 0
        self.show_page()

    @staticmethod
    def retrieve_input(text_box):
        input_value = text_box.get("1.0", "end-1c")
        return input_value


class LeafletPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.prev_button = tk.Button(self, text="Previous", command=master.prev_page)
        self.prev_button.grid(row=1, column=0, padx=30, pady=10)

        self.page_title = tk.Label(self, text="Page " + str(pageCounter))
        self.page_title.grid(row=1, column=1, padx=30, pady=10)

        self.next_button = tk.Button(self, text="Next", command=master.next_page)
        self.next_button.grid(row=1, column=2, padx=30, pady=10)

        self.row1 = PageRow(self, 3)
        self.row2 = PageRow(self, 4)
        self.row3 = PageRow(self, 5)
        self.row4 = PageRow(self, 6)

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
    def __init__(self, master, row_num):
        self.theMaster = master

        self.filename = "WikiNoImage.png"
        self.image = Image.open(self.filename)
        self.resize_image = self.image.resize((150, 150))
        self.photo = ImageTk.PhotoImage(self.resize_image)
        self.label_image = tk.Label(master, image=self.photo)
        self.label_image.image = self.photo
        self.label_image.bind("<Button-1>", self.image_click)

        self.text_box = tk.Text(master, height=9, width=52, wrap="word")
        self.text_box.tag_configure("wrong", foreground="red", underline=True)
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

        self.word_menu = tk.Menu(master, tearoff=0)
        self.word_menu.add_command(label="Copy", command=self.copy_word)
        self.word_menu.add_command(label="Paste", command=self.paste_word)
        self.word_menu.add_separator()

        self.regex = re.compile('[^a-zA-Z]')
        self.replacement_word = ""

        self.sentence_complexity = "Good"
        self.sentence_issues = [False, False]
        self.reading_level = 0
        self.word_length = 0

        self.num_spaces = 0

    def check_sentence(self, event):
        self.reading_level = textstat.flesch_reading_ease(self.text_box.get("1.0", "end-1c"))
        if self.reading_level < 75:
            self.sentence_issues[0] = True
        elif self.reading_level > 75:
            self.sentence_issues[0] = False

        self.word_length = len(self.text_box.get("1.0", "end-1c"))
        if self.word_length > 10:
            self.sentence_issues[1] = True
        elif self.word_length < 10:
            self.sentence_issues[1] = False

        self.update_complexity()

    def update_complexity(self):
        if len(self.sentence_issues) > 0:
            self.sentence_complexity = "Average"
        elif len(self.sentence_issues) > 3:
            self.sentence_complexity = "Bad"
        else:
            self.sentence_complexity = "Good"
        self.update_complexity_image()

    def update_complexity_image(self):
        if self.sentence_complexity == "Good":
            self.complexity_filename = "WikiGreenCircle.png"
        elif self.sentence_complexity == "Average":
            self.complexity_filename = "WikiGreenCircle.png"
        else:
            self.complexity_filename = "WikiRedCircle.png"
        self.complexity_image = Image.open(self.complexity_filename)
        self.complexity_resize_image = self.complexity_image.resize((100, 100))
        self.complexity_photo = ImageTk.PhotoImage(self.complexity_resize_image)
        self.complexity_icon = tk.Label(self.theMaster, image=self.complexity_photo)
        self.complexity_icon.image = self.complexity_photo

    def image_click(self, event=None):
        filetypes = (('image png', '*.png'), ('image jpg', '*.jpg'), ('All files', '*.*'))
        self.filename = fd.askopenfilename(title='Open Images', initialdir='/', filetypes=filetypes)
        self.image = Image.open(self.filename)
        self.resize_image = self.image.resize((150, 150))
        self.photo = ImageTk.PhotoImage(self.resize_image)
        self.label_image.configure(image=self.photo)
        self.label_image.image = self.photo

    def get_row(self):
        return self.filename, self.text_box

    def check_spelling(self, event):
        text = self.text_box.get("1.0", tk.END)
        current_spaces = text.count(' ')
        if current_spaces != self.num_spaces:
            self.num_spaces = current_spaces
            for word in text.split(' '):
                word_positions = [i for i in range(len(text)) if text.startswith(word, i)]
                suggestion = Word.spellcheck(Word(word))
                suggestion_text = suggestion[0]
                suggestion_text = str(suggestion_text).split(" ", 1)[0]
                suggestion_text = self.regex.sub('', suggestion_text)
                word = self.regex.sub('', word)
                for position in word_positions:
                    if suggestion_text != word and suggestion_text != "n":
                        self.text_box.tag_add("wrong", f'1.{position}', f'1.{position + len(word)}')
                    else:
                        self.text_box.tag_remove("wrong", f'1.{position}', f'1.{position + len(word)}')

    def word_right_click(self, event):
        is_wrong = False
        try:
            is_wrong = self.get_word_replacement(event)
            if is_wrong:
                self.word_menu.add_command(label=self.replacement_word, command=self.replace_word)
            self.word_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            if is_wrong:
                self.replace_word(is_wrong)
            self.word_menu.grab_release()

    def get_word_replacement(self, event):
        text = self.text_box.get("@%d,%d wordstart" % (event.x, event.y), "@%d,%d wordend" % (event.x, event.y))
        self.text_box.mark_set("insert", "@%d,%d" % (event.x, event.y))
        self.text_box.mark_set("sel.first", "insert wordstart")
        self.text_box.mark_set("sel.last", "insert wordend")
        word = Word(text)
        suggestion = word.spellcheck()
        suggestion_text = suggestion[0]
        suggestion_text = str(suggestion_text).split(" ", 1)[0]
        suggestion_text = self.regex.sub('', suggestion_text)
        if suggestion_text == "n":
            return False
        elif suggestion_text != text:
            self.replacement_word = suggestion_text
            return True
        else:
            return False

    def copy_word(self):
        self.text_box.clipboard_clear()
        self.text_box.clipboard_append(self.text_box.selection_get())

    def paste_word(self):
        self.text_box.insert(tk.INSERT, self.text_box.clipboard_get())

    def replace_word(self, is_wrong):
        if is_wrong:
            self.text_box.delete("sel.first", "sel.last")
            self.text_box.insert("sel.first", self.replacement_word)
        self.word_menu.delete(self.replacement_word)


def new_file():
    os.execl(sys.executable, sys.executable, *sys.argv)


if __name__ == '__main__':
    app = LeafletCreator()
    app.mainloop()
