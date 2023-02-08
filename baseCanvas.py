import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter.simpledialog import askstring
from textblob import TextBlob
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

        self.saved_folder = ""

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

    def new_file(self):
        print("hello")

    @staticmethod
    def retrieve_input(text_box):
        input_value = text_box.get("1.0", "end-1c")
        return input_value


class LeafletPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.prev_button = tk.Button(self, text="Previous", command=master.prev_page)
        self.prev_button.grid(row=1, column=0, padx=30, pady=10)

        self.add_page_button = tk.Button(self, text="Add Page", command=master.create_page)
        self.add_page_button.grid(row=1, column=1, padx=30, pady=10)

        self.next_button = tk.Button(self, text="Next", command=master.next_page)
        self.next_button.grid(row=1, column=2, padx=30, pady=10)

        self.row1 = PageRow(self, 3)
        self.row2 = PageRow(self, 4)
        self.row3 = PageRow(self, 5)
        self.row4 = PageRow(self, 6)

    def add_row(self, label, text):
        if self.row1.text_box.get("1.0", "end-1c") == "":
            self.row1.labelImage.configure(text=label)
            self.row1.text_box.insert(tk.END, text)
        elif self.row2.text_box.get("1.0", "end-1c") == "":
            self.row2.labelImage.configure(text=label)
            self.row2.text_box.insert(tk.END, text)
        elif self.row3.text_box.get("1.0", "end-1c") == "":
            self.row3.labelImage.configure(text=label)
            self.row3.text_box.insert(tk.END, text)
        elif self.row4.text_box.get("1.0", "end-1c") == "":
            self.row4.labelImage.configure(text=label)
            self.row4.text_box.insert(tk.END, text)
        else:
            print("Error: No more rows available")


class PageRow:
    def __init__(self, master, row_num):
        self.words = open("words.txt").read().splitlines()

        self.filename = "WikiNoImage.png"
        self.image = Image.open(self.filename)
        self.resizeImage = self.image.resize((150, 150))
        self.photo = ImageTk.PhotoImage(self.resizeImage)
        self.labelImage = tk.Label(master, image=self.photo)
        self.labelImage.image = self.photo
        self.labelImage.bind("<Button-1>", self.image_click)
        self.theMaster = master

        self.text_box = tk.Text(master, height=9, width=52)
        self.text_box.tag_configure("wrong", foreground="red", underline=True)
        self.text_box.bind("<space>", self.check_spelling)

        self.labelImage.grid(row=row_num, column=0, padx=60, pady=10)
        self.text_box.grid(row=row_num, column=1, padx=60, pady=10)

        self.word_menu = tk.Menu(master, tearoff=0)
        self.word_menu.add_command(label="Ignore Spell Check", command=self.ignore_spell)
        self.word_menu.suggestions = []

    def image_click(self, event=None):
        filetypes = (('image png', '*.png'), ('image jpg', '*.jpg'), ('All files', '*.*'))
        self.filename = fd.askopenfilename(title='Open Images', initialdir='/', filetypes=filetypes)
        self.image = Image.open(self.filename)
        self.resizeImage = self.image.resize((150, 150))
        self.photo = ImageTk.PhotoImage(self.resizeImage)
        self.labelImage.configure(image=self.photo)
        self.labelImage.image = self.photo

    def get_row(self):
        return self.filename, self.text_box

    def check_spelling(self, event):
        index = self.text_box.search(r'\s', "insert", backwards=True, regexp=True)
        if index == "":
            index = "1.0"
        else:
            index = self.text_box.index("%s+1c" % index)
        word = self.text_box.get(index, "insert")
        if word in self.words:
            self.text_box.tag_remove("wrong", index, "%s+%dc" % (index, len(word)))
        else:
            self.text_box.tag_add("wrong", index, "%s+%dc" % (index, len(word)))

    def word_right_click(self, event):
        try:
            self.word_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.word_menu.grab_release()

    def ignore_spell(self):

        self.text_box.tag_remove("wrong", index, "%s+%dc" % (index, len(word)))

    def ignore_spell(self):
        pass

if __name__ == '__main__':
    app = LeafletCreator()
    app.mainloop()
