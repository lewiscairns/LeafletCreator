from os.path import expanduser

import docxFiles

import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter.simpledialog import askstring
from PIL import Image, ImageTk


def title_file(self, master):
    self.user_title = tk.simpledialog.askstring(" ", "Please enter a title for this file.")
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
    self.current_page = (self.current_page - 1) % len(self.pages)
    self.show_page()


def prev_page(self):
    self.pages[self.current_page].grid_forget()
    self.current_page = (self.current_page + 1) % len(self.pages)
    self.show_page()


def generate(self):
    if self.saved_folder == "":
        folder_selected = fd.askdirectory(title="Select Folder To Generate File", initialdir=expanduser('~/Documents'))
    else:
        folder_selected = fd.askdirectory(title="Select Folder To Generate File", initialdir=self.saved_folder)
    all_rows = []
    page_counter = 0
    for page in self.pages:
        all_rows.append([page_counter])
        for row in page.row1, page.row2, page.row3, page.row4:
            label, text = row.get_row()
            all_rows[page_counter].append([label, text])
        page_counter = page_counter + 1
    docxFiles.create_document(self.user_title, all_rows, folder_selected, self.font_style, self.font_size, self.watermark_image, self.watermark_text)
    tk.messagebox.showinfo("Success", "Your document has been created, please open it in Word")


class ChangeFont:
    def __init__(self, master):
        self.master = master
        self.top = tk.Toplevel(master)
        self.top.geometry("150x200")
        self.top.title("Font Style")
        self.top_label = tk.Label(self.top, text="The current style is: " + self.master.font_style)
        self.arial_button = tk.Button(self.top, text="Arial", command=self.arial)
        self.times_button = tk.Button(self.top, text="Times New Roman", command=self.times)
        self.helvetica_button = tk.Button(self.top, text="Helvetica", command=self.helvetica)
        self.calibri_button = tk.Button(self.top, text="Calibri", command=self.calibri)
        self.top_label.grid(row=0, column=0, padx=10, pady=5)
        self.arial_button.grid(row=1, column=0, padx=10, pady=5)
        self.times_button.grid(row=2, column=0, padx=10, pady=5)
        self.helvetica_button.grid(row=3, column=0, padx=10, pady=5)
        self.calibri_button.grid(row=4, column=0, padx=10, pady=5)

    def arial(self):
        self.master.font_style = "Arial"
        self.top.destroy()
        tk.messagebox.showinfo("Success", "Your document will now generate in Arial as the font style")

    def times(self):
        self.master.font_style = "Times New Roman"
        self.top.destroy()
        tk.messagebox.showinfo("Success", "Your document will now generate in Times New Roman as the font style")

    def helvetica(self):
        self.master.font_style = "Helvetica"
        self.top.destroy()
        tk.messagebox.showinfo("Success", "Your document will now generate in Helvetica as the font style")

    def calibri(self):
        self.master.font_style = "Calibri"
        self.top.destroy()
        tk.messagebox.showinfo("Success", "Your document will now generate in Calibri as the font style")


class ChangeFontSize:
    def __init__(self, master):
        self.master = master
        self.top = tk.Toplevel(master)
        self.top.geometry("180x80")
        self.top.title("Font Size")
        self.top_label = tk.Label(self.top, text="Recommended Font Size is 18")
        self.top_button_up = tk.Button(self.top, text="+", command=self.increase_font_size)
        self.top_button_down = tk.Button(self.top, text="-", command=self.decrease_font_size)
        self.top_font_size = tk.IntVar()
        self.top_font_size.set(self.master.font_size)
        self.top_entry = tk.Entry(self.top, textvariable=self.top_font_size)
        self.top_entry.configure(state="readonly")
        self.top_button = tk.Button(self.top, text="Close", command=self.top.destroy)
        self.top_label.grid(row=0, column=0, columnspan=3)
        self.top_button_up.grid(row=1, column=0)
        self.top_entry.grid(row=1, column=1)
        self.top_button_down.grid(row=1, column=2)
        self.top_button.grid(row=2, column=1)

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
        self.top.geometry("220x80")
        self.top.title("Reading Level")
        self.top_label = tk.Label(self.top, text="Recommended Reading Level is 90")
        self.top_button_up = tk.Button(self.top, text="+", command=self.increase_reading_level)
        self.top_button_down = tk.Button(self.top, text="-", command=self.decrease_reading_level)
        self.top_reading_level = tk.IntVar()
        self.top_reading_level.set(self.master.reading_level)
        self.top_entry = tk.Entry(self.top, textvariable=self.top_reading_level)
        self.top_entry.configure(state="readonly")
        self.top_button = tk.Button(self.top, text="Close", command=self.top.destroy)
        self.top_label.grid(row=0, column=0, columnspan=3)
        self.top_button_up.grid(row=1, column=0)
        self.top_entry.grid(row=1, column=1)
        self.top_button_down.grid(row=1, column=2)
        self.top_button.grid(row=2, column=1)

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
        self.top.geometry("220x80")
        self.top.title("Word Count")
        self.top_label = tk.Label(self.top, text="Recommended Word Count is 15")
        self.top_button_up = tk.Button(self.top, text="+", command=self.increase_word_count)
        self.top_button_down = tk.Button(self.top, text="-", command=self.decrease_word_count)
        self.top_word_count = tk.IntVar()
        self.top_word_count.set(self.master.word_count)
        self.top_entry = tk.Entry(self.top, textvariable=self.top_word_count)
        self.top_entry.configure(state="readonly")
        self.top_button = tk.Button(self.top, text="Close", command=self.top.destroy)
        self.top_label.grid(row=0, column=0, columnspan=3)
        self.top_button_up.grid(row=1, column=0)
        self.top_entry.grid(row=1, column=1)
        self.top_button_down.grid(row=1, column=2)
        self.top_button.grid(row=2, column=1)

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
        self.top.geometry("300x100")
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
        self.top_label.grid(row=0, column=0, columnspan=3)
        self.top_label2.grid(row=1, column=0, columnspan=3)
        self.top_button_up.grid(row=2, column=0)
        self.top_entry.grid(row=2, column=1)
        self.top_button_down.grid(row=2, column=2)
        self.top_button.grid(row=3, column=1)

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
        self.top.geometry("220x150")
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


class WhatEasyRead:
    def __init__(self, master):
        self.master = master
        self.top = tk.Toplevel(master)
        self.top.geometry("600x300")
        self.top.title("What is Easy Read?")
        self.top_label = tk.Label(self.top, text="Focus on key message")
        self.top_label2 = tk.Label(self.top, text="Find the key message that is being conveyed, \n removing the information that isn’t useful to this key message.\n")
        self.top_label3 = tk.Label(self.top, text="Put message into Easy Read form")
        self.top_label4 = tk.Label(self.top, text="Take the message and put it into simple English, and make sure to split \n the content into multiple documents if one is too long, as too not overwhelm the reader.\n")
        self.top_label5 = tk.Label(self.top, text="Make sure it is Easy to Read")
        self.top_label6 = tk.Label(self.top, text="Ensure jargon and acronyms are explained or removed, \n and test your content on people with learning disabilities.\n")
        self.top_button = tk.Button(self.top, text="Close", command=self.top.destroy)
        self.top_label.configure(font=("Arial", 12, "bold"))
        self.top_label2.configure(font=("Arial", 12))
        self.top_label3.configure(font=("Arial", 12, "bold"))
        self.top_label4.configure(font=("Arial", 12))
        self.top_label5.configure(font=("Arial", 12, "bold"))
        self.top_label6.configure(font=("Arial", 12))
        self.top_label.grid(row=0, column=0, columnspan=2)
        self.top_label2.grid(row=1, column=0, columnspan=2)
        self.top_label3.grid(row=2, column=0, columnspan=2)
        self.top_label4.grid(row=3, column=0, columnspan=2)
        self.top_label5.grid(row=4, column=0, columnspan=2)
        self.top_label6.grid(row=5, column=0, columnspan=2)
        self.top_button.grid(row=6, column=0, columnspan=2)


class EnglishEasyRead:
    def __init__(self, master):
        self.master = master
        self.top = tk.Toplevel(master)
        self.top.geometry("680x465")
        self.top.title("English EasyRead")
        self.top_label = tk.Label(self.top, text="Keep information clear")
        self.top_label2 = tk.Label(self.top, text="Write information in a logical order, as if you were speaking it to the \n reader, and in sentences that aren’t too long, with 15 words being a good limit.\n")
        self.top_label3 = tk.Label(self.top, text="Deal with technical terms")
        self.top_label4 = tk.Label(self.top, text="Technical terms may need to be included, and these should be explained, \n which can be done in a glossary rather than repeating the explanation over and over.\n")
        self.top_label5 = tk.Label(self.top, text="Simplify punctuation")
        self.top_label6 = tk.Label(self.top, text="Use simple punctuation, such as commas and full stops, while avoiding less common ones such \n as colons and dashes, and split the sentence or use bullet points instead of too many commas.\n")
        self.top_label7 = tk.Label(self.top, text="Use personal language")
        self.top_label8 = tk.Label(self.top, text="Personal language such as “I”, “You”, and “We” while being explicate over \n who these mean, for example “We in this document means the NHS”.\n")
        self.top_label9 = tk.Label(self.top, text="Avoid percentages and numerals")
        self.top_label10 = tk.Label(self.top, text="Using generalized words such as “Most” instead of exact percentages and words \n over numerals such as “three” instead of “3” makes your document easier to understand.\n")
        self.top_button = tk.Button(self.top, text="Close", command=self.top.destroy)
        self.top_label.configure(font=("Arial", 12, "bold"))
        self.top_label2.configure(font=("Arial", 12))
        self.top_label3.configure(font=("Arial", 12, "bold"))
        self.top_label4.configure(font=("Arial", 12))
        self.top_label5.configure(font=("Arial", 12, "bold"))
        self.top_label6.configure(font=("Arial", 12))
        self.top_label7.configure(font=("Arial", 12, "bold"))
        self.top_label8.configure(font=("Arial", 12))
        self.top_label9.configure(font=("Arial", 12, "bold"))
        self.top_label10.configure(font=("Arial", 12))
        self.top_label.grid(row=0, column=0, columnspan=2)
        self.top_label2.grid(row=1, column=0, columnspan=2)
        self.top_label3.grid(row=2, column=0, columnspan=2)
        self.top_label4.grid(row=3, column=0, columnspan=2)
        self.top_label5.grid(row=4, column=0, columnspan=2)
        self.top_label6.grid(row=5, column=0, columnspan=2)
        self.top_label7.grid(row=6, column=0, columnspan=2)
        self.top_label8.grid(row=7, column=0, columnspan=2)
        self.top_label9.grid(row=8, column=0, columnspan=2)
        self.top_label10.grid(row=9, column=0, columnspan=2)
        self.top_button.grid(row=10, column=0, columnspan=2)


class ContentEasyRead:
    def __init__(self, master):
        self.master = master
        self.top = tk.Toplevel(master)
        self.top.geometry("750x230")
        self.top.title("Content EasyRead")
        self.top_label = tk.Label(self.top, text="Try not to confuse the reader")
        self.top_label2 = tk.Label(self.top, text="Writing in facts is better than metaphors, as metaphors can confuse the reader instead of helping \n the reader, being simple and direct while keeping ideas or actions to one sentence is best.")
        self.top_label3 = tk.Label(self.top, text="Be clear and consistent")
        self.top_label4 = tk.Label(self.top, text="Language used in the document should be kept consistent, such as not switching between “doctor” and \n “GP”, and ensure that it is clear what is information and what requires action from the reader.")
        self.top_label5 = tk.Label(self.top, text="Use bold when needed")
        self.top_label6 = tk.Label(self.top, text="To highlight import words, bold can be used, but remember that not everyone will notice this.")
        self.top_button = tk.Button(self.top, text="Close", command=self.top.destroy)
        self.top_label.configure(font=("Arial", 12, "bold"))
        self.top_label2.configure(font=("Arial", 12))
        self.top_label3.configure(font=("Arial", 12, "bold"))
        self.top_label4.configure(font=("Arial", 12))
        self.top_label5.configure(font=("Arial", 12, "bold"))
        self.top_label6.configure(font=("Arial", 12))
        self.top_label.grid(row=0, column=0, columnspan=2)
        self.top_label2.grid(row=1, column=0, columnspan=2)
        self.top_label3.grid(row=2, column=0, columnspan=2)
        self.top_label4.grid(row=3, column=0, columnspan=2)
        self.top_label5.grid(row=4, column=0, columnspan=2)
        self.top_label6.grid(row=5, column=0, columnspan=2)
        self.top_button.grid(row=6, column=0, columnspan=2)


class DoEasyRead:
    def __init__(self, master):
        self.master = master
        self.top = tk.Toplevel(master)
        self.top.geometry("550x600")
        self.top.title("Do EasyRead")
        self.top_label = tk.Label(self.top, text="Words are useful for:")
        self.top_label2 = tk.Label(self.top, text="o  Explaining in detail \no  Giving lots of information \no  Ensure there is as little mis-understanding as possible \n")
        self.top_label3 = tk.Label(self.top, text="Pictures are useful for:")
        self.top_label4 = tk.Label(self.top, text="o  Understood by anyone no matter their reading level \no  Support the ideas in the text \no  Show a key person, object, action, or place \no  More interesting and digestible for the reader \n")
        self.top_label5 = tk.Label(self.top, text="Avoid using:")
        self.top_label6 = tk.Label(self.top, text="o  Jargon and hard / uncommon words \no  Putting words in all capitals \no  Pictures were colour blind people may not understand the meaning \no  Avoid abstracting who is being talked to, use “You” over “One” for example \no  Blurred or overly convoluted pictures \no  Symbolic or abstract pictures \n")
        self.top_label7 = tk.Label(self.top, text="Try using:")
        self.top_label8 = tk.Label(self.top, text="o  “Do not”, “can not”, and “would not” over “don’t”, “can’t”, “won’t” as \n some readers may require the word not in the sentence to understand it \no  The word for “percent” or “pound” over “%” and “£” \no  Pictures that support the text, not take away from it \no  Pictures that are clear and easy to understand \no  Pictures that are not too busy \n")
        self.top_button = tk.Button(self.top, text="Close", command=self.top.destroy)
        self.top_label.configure(font=("Arial", 12, "bold"))
        self.top_label2.configure(font=("Arial", 12))
        self.top_label3.configure(font=("Arial", 12, "bold"))
        self.top_label4.configure(font=("Arial", 12))
        self.top_label5.configure(font=("Arial", 12, "bold"))
        self.top_label6.configure(font=("Arial", 12))
        self.top_label7.configure(font=("Arial", 12, "bold"))
        self.top_label8.configure(font=("Arial", 12))
        self.top_label.grid(row=0, column=0, columnspan=2)
        self.top_label2.grid(row=1, column=0, columnspan=2)
        self.top_label3.grid(row=2, column=0, columnspan=2)
        self.top_label4.grid(row=3, column=0, columnspan=2)
        self.top_label5.grid(row=4, column=0, columnspan=2)
        self.top_label6.grid(row=5, column=0, columnspan=2)
        self.top_label7.grid(row=6, column=0, columnspan=2)
        self.top_label8.grid(row=7, column=0, columnspan=2)
        self.top_button.grid(row=8, column=0, columnspan=2)
