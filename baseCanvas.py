import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter.simpledialog import askstring
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

    def title_file(self):
        self.user_title = tk.simpledialog.askstring("File Name", "Please enter a title for this file")
        new_title = self.user_title + " - Leaflet Creator"
        LeafletCreator.title(self, new_title)

    def create_page(self):
        global pageCounter
        self.pages.append(LeafletPage(self))
        pageCounter = pageCounter + 1
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
        all_rows = [[]]
        page_counter = 0
        for page in self.pages:
            all_rows.append([page_counter])
            for row in page.row1, page.row2, page.row3, page.row4:
                label, text = row.get_row()
                all_rows[page_counter].append([label, self.retrieve_input(text)])
            page_counter = page_counter + 1
        all_rows.pop(1)
        docxFiles.create_document(self.user_title, all_rows, folder_selected)
        tk.messagebox.showinfo("Success", "Your document has been created, please open it in Word")

    def move_page(self):
        print("Move Page")

    def save_as(self):
        try:
            self.saved_folder = fd.askdirectory(title="Select Folder To Generate File")
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
                tk.messagebox.showinfo("Success", "Your document has been saved")
        except Exception as e:
            print("Error: " + str(e))

    def save(self):
        try:
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
        except Exception as e:
            print("Error: " + str(e))

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

        self.title_button = tk.Button(self, text="Title", command=master.title_file)
        self.title_button.grid(row=0, column=0, padx=30, pady=10)

        self.add_button = tk.Button(self, text="Add New Page", command=master.create_page)
        self.add_button.grid(row=0, column=1, padx=30, pady=10)

        self.page_move_button = tk.Button(self, text="Move Page", command=master.move_page)
        self.page_move_button.grid(row=0, column=2, padx=30, pady=10)

        self.prev_button = tk.Button(self, text="Previous", command=master.prev_page)
        self.prev_button.grid(row=1, column=0, padx=30, pady=10)

        self.next_button = tk.Button(self, text="Next", command=master.next_page)
        self.next_button.grid(row=1, column=1, padx=30, pady=10)

        self.generate_button = tk.Button(self, text="Generate", command=master.generate)
        self.generate_button.grid(row=1, column=2, padx=30, pady=10)

        self.save_button = tk.Button(self, text="Save", command=master.save)
        self.save_button.grid(row=2, column=0, padx=30, pady=10)

        self.load_button = tk.Button(self, text="Load", command=master.load)
        self.load_button.grid(row=2, column=1, padx=30, pady=10)

        self.save_as_button = tk.Button(self, text="Save As", command=master.save_as)
        self.save_as_button.grid(row=2, column=2, padx=30, pady=10)

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
        self.filename = "WikiNoImage.png"
        self.image = Image.open(self.filename)
        self.resizeImage = self.image.resize((150, 150))
        self.photo = ImageTk.PhotoImage(self.resizeImage)
        self.labelImage = tk.Label(master, image=self.photo)
        self.labelImage.image = self.photo
        self.labelImage.bind("<Button-1>", self.image_click)
        self.theMaster = master

        self.text_box = tk.Text(master, height=9, width=52)

        self.labelImage.grid(row=row_num, column=0, padx=60, pady=10)
        self.text_box.grid(row=row_num, column=1, padx=60, pady=10)

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


if __name__ == '__main__':
    app = LeafletCreator()
    app.mainloop()
