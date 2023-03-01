import tkinter as tk

import textstat
from textblob import TextBlob
import numpy as np
from PIL import Image, ImageTk


def show_complexity_recommendations(self):
    recommendation_text = ""
    for recommendation in self.complexity_recommendations:
        if recommendation != "":
            recommendation_text += "\n" + recommendation
    if recommendation_text == "":
        recommendation_text = "No recommendations available"
    top = tk.Toplevel(self.master)
    top.geometry("300x250")
    top.title("Recommendations")
    top_label = tk.Label(top, text=recommendation_text)
    top_button = tk.Button(top, text="Close", command=top.destroy)
    top_label.pack()
    top_button.pack()


def check_sentence(self):
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

    self.polarity = TextBlob(self.text_box.get("1.0", "end-1c")).sentiment.polarity
    if self.polarity < self.leaflet_master.polarity:
        self.sentence_issues[2] = True
        self.complexity_recommendations[2] = "Current polarity (how positive your sentence is) is: " + str(
            round(self.polarity, 2)) + "\nTry keep it above " + str(self.leaflet_master.polarity) + ".\n"
    elif self.polarity > self.leaflet_master.polarity:
        self.sentence_issues[2] = False
        self.complexity_recommendations[2] = ""

    update_complexity(self)


def update_complexity(self):
    if np.count_nonzero(self.sentence_issues) > 1:
        self.sentence_complexity = "Bad"
    elif np.count_nonzero(self.sentence_issues) > 0:
        self.sentence_complexity = "Average"
    else:
        self.sentence_complexity = "Good"
    update_complexity_image(self)


def update_complexity_image(self):
    if self.sentence_complexity == "Good":
        self.complexity_filename = "images/WikiGreenCircle.png"
    elif self.sentence_complexity == "Average":
        self.complexity_filename = "images/WikiYellowCircle.png"
    else:
        self.complexity_filename = "images/WikiRedCircle.png"

    self.complexity_image = Image.open(self.complexity_filename)
    self.complexity_resize_image = self.complexity_image.resize((100, 100))
    self.complexity_photo = ImageTk.PhotoImage(self.complexity_resize_image)
    self.complexity_icon.configure(image=self.complexity_photo)
    self.complexity_icon.image = self.complexity_photo
