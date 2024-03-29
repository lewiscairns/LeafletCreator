# Import necessary libraries and modules
import tkinter as tk

import textstat
from textblob import TextBlob
import numpy as np
from PIL import Image, ImageTk


# This function is used to show the complexity advice of the sentences in the text box
def show_complexity_recommendations(self):
    recommendation_text = ""

    # The for loop is used to check if there are any recommendations to be made
    for recommendation in self.complexity_recommendations:
        if recommendation != "":
            recommendation_text += "\n" + recommendation
    if recommendation_text == "":
        recommendation_text = "No recommendations available"

    # Creates a new window to show the recommendations
    top = tk.Toplevel(self.master)
    top.geometry("300x400")
    top.title("Recommendations")
    top_label = tk.Label(top, text=recommendation_text)
    top_button = tk.Button(top, text="Close", command=top.destroy)
    top_label.pack()
    top_button.pack()


# This function is used to check the complexity of the sentences in the text box
def check_sentence(self):
    # These variables are used to store the complexity of the sentences
    sentences = self.text_box.get("1.0", "end-1c").split(".")
    sentence_warnings = [False, False, False, False]
    self.complexity_recommendations = []
    x = 0

    # This for loop is used to check the complexity of each sentence
    for sentence in sentences:
        x = x+1
        recommendation_text = "Recommendations for sentence " + str(x) + " in this box:\n \n"

        # Check the sentence against each rule, and if it is broken then add a recommendation and change the sentence issues array
        self.reading_level = textstat.flesch_reading_ease(sentence)
        if self.reading_level < self.leaflet_master.reading_level:
            self.sentence_issues[0] = True
            sentence_warnings[0] = True
            recommendation_text += "Reading level is: " + str(
                round(self.reading_level)) + "\nTry keep it above " + str(self.leaflet_master.reading_level) + "\n \n"
        elif sentence_warnings[0] is False:
            self.sentence_issues[0] = False

        self.word_count = len(sentence.split())
        if self.word_count > self.leaflet_master.word_count:
            self.sentence_issues[1] = True
            sentence_warnings[1] = True
            recommendation_text += "Current word count is: " + str(
                self.word_count) + "\nTry keep it below " + str(self.leaflet_master.word_count) + " words.\n \n"
        elif sentence_warnings[1] is False:
            self.sentence_issues[1] = False

        self.polarity = TextBlob(sentence).sentiment.polarity
        if self.polarity < self.leaflet_master.polarity:
            self.sentence_issues[2] = True
            sentence_warnings[2] = True
            recommendation_text += "Current sentiment rating (Positivity rating) is: " + str(
                round(self.polarity, 2)) + "\nTry keep it above " + str(self.leaflet_master.polarity) + "\n \n"
        elif sentence_warnings[2] is False:
            self.sentence_issues[2] = False

        self.grammatical_detection = check_for_complex_grammar(self, sentence.split())
        if self.grammatical_detection != "":
            self.sentence_issues[3] = True
            sentence_warnings[3] = True
            recommendation_text += "You have used a complex grammatical word: " + self.grammatical_detection + "\n" + "Try splitting this sentence into 2 instead.\n \n"
        elif sentence_warnings[3] is False:
            self.sentence_issues[3] = False

        if recommendation_text == "Recommendations for sentence " + str(x) + " in this box:\n \n":
            recommendation_text = ""
        self.complexity_recommendations.append(recommendation_text)
    update_complexity(self)


# This function is used to update the current number of issues in the sentence
def update_complexity(self):
    if np.count_nonzero(self.sentence_issues) > 1:
        self.sentence_complexity = "Bad"
    elif np.count_nonzero(self.sentence_issues) > 0:
        self.sentence_complexity = "Average"
    else:
        self.sentence_complexity = "Good"
    update_complexity_image(self)


# This function is used to update the complexity image of the sentences in the row
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


# This function is used to check if the sentence contains any complex grammar
def check_for_complex_grammar(self, sentence):
    complex_grammar = ""
    for word in sentence:
        if word.lower() in self.leaflet_master.complex_grammar_list:
            complex_grammar = word
    return complex_grammar
