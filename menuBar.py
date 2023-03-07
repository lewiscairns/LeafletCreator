import docxFiles

import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter.simpledialog import askstring
from PIL import Image, ImageTk


def new_file(self):
    pass


def title_file(self, master):
    self.user_title = tk.simpledialog.askstring("File Name", "Please enter a title for this file")
    new_title = self.user_title + " - Leaflet Creator"
    master.title(self, new_title)


def create_page(self, master_page):
    self.page_counter = self.page_counter + 1
    self.pages.append(master_page(self))
    self.pages[self.current_page].grid_forget()
    self.current_page = len(self.pages) - 1
    self.show_page()


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
    docxFiles.create_document(self.user_title, all_rows, folder_selected, self.font_style, self.font_size, self.watermark_image, self.watermark_text)
    tk.messagebox.showinfo("Success", "Your document has been created, please open it in Word")


def move_page(self):
    pass


class ChangeFont:
    def __init__(self, master):
        self.master = master
        self.top = tk.Toplevel(master)
        self.top.geometry("300x150")
        self.top.title("Font Style")
        self.top_label = tk.Label(self.top, text="The current style is: " + self.master.font_style)
        self.arial_button = tk.Button(self.top, text="Arial", command=self.arial)
        self.times_button = tk.Button(self.top, text="Times New Roman", command=self.times)
        self.top_label.grid(row=0, column=0, padx=10, pady=5)
        self.arial_button.grid(row=1, column=0, padx=10, pady=5)
        self.times_button.grid(row=2, column=0, padx=10, pady=5)

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
        self.top_label = tk.Label(self.top, text="Recommended Font Size is 18")
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
        if self.master.font_size == 24:
            pass
        else:
            self.master.font_size = self.master.font_size + 1
            self.top_font_size.set(self.master.font_size)

    def decrease_font_size(self):
        if self.master.font_size == 12:
            pass
        else:
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
        if self.master.reading_level == 120:
            pass
        else:
            self.master.reading_level = self.master.reading_level + 1
            self.top_reading_level.set(self.master.reading_level)

    def decrease_reading_level(self):
        if self.master.reading_level == 0:
            pass
        else:
            self.master.reading_level = self.master.reading_level - 1
            self.top_reading_level.set(self.master.reading_level)


class ChangeWordCount:
    def __init__(self, master):
        self.master = master
        self.top = tk.Toplevel(master)
        self.top.geometry("300x150")
        self.top.title("Word Count")
        self.top_label = tk.Label(self.top, text="Recommended Word Count is 15")
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
        if self.master.word_count == 25:
            pass
        else:
            self.master.word_count = self.master.word_count + 1
            self.top_word_count.set(self.master.word_count)

    def decrease_word_count(self):
        if self.master.word_count == 1:
            pass
        else:
            self.master.word_count = self.master.word_count - 1
            self.top_word_count.set(self.master.word_count)


class ChangeSentiment:
    def __init__(self, master):
        self.master = master
        self.top = tk.Toplevel(master)
        self.top.geometry("300x150")
        self.top.title("Sentiment Rating")
        self.top_label = tk.Label(self.top, text="Recommended Sentiment Rating is 0")
        self.top_label2 = tk.Label(self.top, text="Most positive rating is 1, most negative rating is -1")
        self.top_button_up = tk.Button(self.top, text="+", command=self.increase_polarity_limit)
        self.top_button_down = tk.Button(self.top, text="-", command=self.decrease_polarity_limit)
        self.top_polarity = tk.IntVar()
        self.top_polarity.set(self.master.polarity)
        self.top_entry = tk.Entry(self.top, textvariable=self.top_polarity)
        self.top_entry.configure(state="readonly")
        self.top_button = tk.Button(self.top, text="Close", command=self.top.destroy)
        self.top_label.grid(row=0, column=0, columnspan=2)
        self.top_label2.grid(row=1, column=0, columnspan=2)
        self.top_button_up.grid(row=2, column=0)
        self.top_entry.grid(row=2, column=1)
        self.top_button_down.grid(row=2, column=2)
        self.top_button.grid(row=3, column=0, columnspan=2)

    def increase_polarity_limit(self):
        if self.master.polarity == 1:
            pass
        else:
            self.master.polarity = self.master.polarity + 0.1
            self.top_polarity.set(self.master.polarity)

    def decrease_polarity_limit(self):
        if self.master.polarity == -1:
            pass
        else:
            self.master.polarity = self.master.polarity - 0.1
            self.top_polarity.set(self.master.polarity)


class Footer:
    def __init__(self, master):
        self.master = master
        self.watermark_image = self.master.watermark_image
        self.top = tk.Toplevel(master)
        self.top.geometry("300x150")
        self.top.title("Footer")
        self.top_label = tk.Label(self.top, text="Please enter watermark text and image")
        self.top_button = tk.Button(self.top, text="Close", command=self.top.destroy)
        self.top_button_save = tk.Button(self.top, text="Save", command=self.save_watermark)
        self.watermark_text = tk.StringVar()
        self.watermark_text.set(self.master.watermark_text)
        self.top_entry = tk.Entry(self.top, textvariable=self.watermark_text)
        self.top_image = Image.open(self.watermark_image)
        self.top_resize_image = self.top_image.resize((50, 50))
        self.top_photo = ImageTk.PhotoImage(self.top_resize_image)
        self.top_image_label = tk.Label(self.top, image=self.top_photo, cursor="hand2")
        self.top_image_label.bind("<Button-1>", self.image_click)
        self.top_label.grid(row=0, column=0, columnspan=2)
        self.top_entry.grid(row=1, column=0, padx=5, pady=10)
        self.top_image_label.grid(row=1, column=1, padx=10, pady=10)
        self.top_button_save.grid(row=2, column=0, pady=10)
        self.top_button.grid(row=2, column=1, pady=10)

    def save_watermark(self):
        self.master.watermark_text = self.top_entry.get()
        self.master.watermark_image = self.watermark_image
        self.top.destroy()

    # noinspection PyUnusedLocal
    def image_click(self, event):
        filetypes = (('image png', '*.png'), ('image jpg', '*.jpg'), ('All files', '*.*'))
        self.watermark_image = fd.askopenfilename(title='Open Images',
                                                  initialdir='C:/Program Files/LeafletCreator/Images',
                                                  filetypes=filetypes)
        self.top_image = Image.open(self.watermark_image)
        self.top_resize_image = self.top_image.resize((50, 50))
        self.top_photo = ImageTk.PhotoImage(self.top_resize_image)
        self.top_image_label.configure(image=self.top_photo)
        self.top_image_label.image = self.top_photo
        self.top.lift()
