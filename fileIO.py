# Import necessary libraries and modules
import pickle as lc
import tkinter as tk
from os.path import expanduser
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

import complexityAnalysis
import rightClickMenu


# This function is used to get a folder to save the file
def save_as(self):
    # This try statement is used to get the folder to save the file in, then send it to be saved
    try:
        self.saved_folder = fd.askdirectory(title="Select Folder To Generate File", initialdir=expanduser('~/Documents'))
        saving(self)
        tk.messagebox.showinfo("Success", "Your document has been saved")
    except Exception as e:
        print("Error: " + str(e))


# This function is used to save the leaflet if it has already been saved before
def save(self):
    try:
        if self.saved_folder == "":
            save_as(self)
        saving(self)
    except Exception as e:
        print("Error: " + str(e))


# This function is used to save the leaflet
def saving(self):
    # Open the folder and declare the file name
    with open(self.saved_folder + "/" + self.user_title + ".lc", "wb") as file:
        pages_text = []
        # Open each page
        for page in self.pages:
            page_text = []
            # Get the text and image from each row and add it to the list
            for row in page.row1, page.row2, page.row3, page.row4:
                label, text = row.get_row()
                page_text.append([label, self.retrieve_input(text)])
            # Add the text and images to the array of all the pages
            pages_text.append(page_text)

        # Save the data to the file
        data = [self.user_title, self.font_size, self.font_style, self.word_count, self.reading_level,
                self.ignore_words, self.polarity, self.watermark_text,
                self.watermark_image, self.saved_folder, pages_text]
        lc.dump(data, file, protocol=lc.HIGHEST_PROTOCOL)


# This function is used to load a leaflet
def load(self, master, master_page):
    # Remove the current files GUI
    self.pages[self.current_page].grid_forget()

    # Get the file to load
    filetypes = (('leaflet.lc', '*.lc'), ('All files', '*.*'))
    filename = fd.askopenfilename(title='Open Leaflet', initialdir=expanduser('~/Documents'), filetypes=filetypes)
    try:
        # Open the file and load the data
        with open(filename, "rb") as file:
            data = lc.load(file)
            self.user_title = data[0]
            self.font_size = data[1]
            self.font_style = data[2]
            self.word_count = data[3]
            self.reading_level = data[4]
            self.ignore_words = data[5]
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
    
    # Update the GUI
    self.current_page = 0
    self.show_page()
    
    # Check the spelling and complexity of the text
    for page in self.pages:
        for row in page.row1, page.row2, page.row3, page.row4:
            rightClickMenu.check_spelling(row)
            complexityAnalysis.check_sentence(row)
