import pickle as lc
import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo


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
        data = [self.user_title, self.font_size, self.font_style, self.word_count, self.reading_level,
                self.ignore_uncommon_words, self.polarity, self.watermark_text,
                self.watermark_image, self.saved_folder, pages_text]
        lc.dump(data, file, protocol=lc.HIGHEST_PROTOCOL)


def load(self, master, master_page):
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
            self.polarity = data[6]
            self.watermark_text = data[7]
            self.watermark_image = data[8]
            self.saved_folder = data[9]
            new_title = (self.user_title + " - Leaflet Creator")
            master.title(self, new_title)
            self.pages = []
            self.page_counter = 0
            for page in data[10]:
                self.page_counter += 1
                self.pages.append(master_page(self))
                for row in page:
                    self.pages[self.page_counter-1].add_row(row[0], row[1])
    except Exception as e:
        print("Error: " + str(e))
    self.current_page = 0
    self.show_page()
