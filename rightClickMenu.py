# Import necessary libraries and modules
import tkinter as tk

from textblob import Word
from nltk.corpus import wordnet
import re


# This function checks the spelling of the text
def check_spelling(self):
    # Get the text from the text box
    self.text = self.text_box.get("1.0", tk.END)
    self.misspelled_tag = []

    # Loop through each word in the text
    for word in self.text.split(' '):
        # Make the word lowercase and get its position
        word = word.lower()
        word_positions = [word_start for word_start in range(len(self.text)-len(word)+1) if self.text[word_start:word_start+len(word)] == word]

        # Get the suggestion to replace the word and parse it
        suggestion = Word.spellcheck(Word(word))
        suggestion_text = suggestion[0]
        suggestion_text = str(suggestion_text).split(" ", 1)[0]
        suggestion_text = self.regex.sub('', suggestion_text)

        # Parse the word
        word = re.sub(r'[.;:,?"!/]', '', word)
        word_parsed = self.regex.sub('', word)

        # Loop through each position of the word
        for position in word_positions:

            # Store the words position
            self.misspelled_tag.append(position)
            word_found = find_word_in_list(suggestion, word_parsed)

            # Check if the word is misspelled and add the wrong tag to it
            if suggestion_text != "n" and word_found is False and word_parsed != "\n" and word_parsed.isspace() is False and len(word_parsed) \
                    != 1 and word not in self.leaflet_master.ignore_words and word != "-":
                self.text_box.tag_add("wrong", f'1.{position}', f'1.{position + len(word)}')
            else:
                # Remove the wrong tag and word position if the word is not misspelled
                self.text_box.tag_remove("wrong", f'1.{position}', f'1.{position + len(word)}')
                self.misspelled_tag.remove(position)
    word_complexity_check(self)


# This function checks the complexity of the text
def word_complexity_check(self):
    # Get the text from the text box
    for word in self.text.split(' '):
        # Get the position of the word, and parse it
        word_positions = [word_start for word_start in range(len(self.text)-len(word)+1) if self.text[word_start:word_start+len(word)] == word]
        word = word.lower()
        word = re.sub(r'[.;:,?"!/]', '', word)
        word_parsed = self.regex.sub('', word)

        # Loop through each position of the word
        for position in word_positions:
            # Check if the word is wrong instead of uncommon, and add an uncommon tag to it
            if get_word_synonym(self, word_parsed) and len(self.synonyms) == 0 and word not in self.leaflet_master.ignore_words and word != "-":
                self.text_box.tag_remove("uncommon", f'1.{position}', f'1.{position + len(word)}')
                self.text_box.tag_add("wrong", f'1.{position}', f'1.{position + len(word)}')
                self.misspelled_tag.append(position)
            # Check if the word is uncommon, and add an uncommon tag to it, or remove the tag if it isn't
            elif word_parsed in self.leaflet_master.common_words or word in self.leaflet_master.ignore_words or position in self.misspelled_tag:
                self.text_box.tag_remove("uncommon", f'1.{position}', f'1.{position + len(word)}')
            else:
                self.text_box.tag_add("uncommon", f'1.{position}', f'1.{position + len(word)}')


# This function checks if the word is the same as the suggestion
def find_word_in_list(suggestion, word):
    for suggestionWord in suggestion:
        if word == suggestionWord[0]:
            return True
    return False


# This function generates the right-click menu
def word_right_click(self, event):

    # Get the word that was right-clicked
    word = self.text_box.get("@%d,%d wordstart" % (event.x, event.y), "@%d,%d wordend" % (event.x, event.y))
    self.text_box.mark_set("insert", "@%d,%d" % (event.x, event.y))

    # Set the selection to the word that was right-clicked
    self.text_box.mark_set("sel.first", "insert wordstart")
    self.text_box.mark_set("sel.last", "insert wordend")
    wrong_ranges = self.text_box.tag_ranges("wrong")
    uncommon_ranges = self.text_box.tag_ranges("uncommon")
    word_menu = tk.Menu(self.master, tearoff=0)

    # Add the commands to the right-click menu
    word_menu.add_command(label="Copy", command=lambda: copy_word(self))
    word_menu.add_command(label="Paste", command=lambda: paste_word(self))
    word_menu.add_command(label="Bold", command=lambda: bold_word(self))
    is_wrong = False
    is_uncommon = False

    # Check if the word is misspelled or uncommon
    for i in range(0, len(wrong_ranges), 2):
        if str(self.text_box.index("sel.first")) == str(wrong_ranges[i]):
            is_wrong = True
            get_word_replacement(self, word)
            break
    for i in range(0, len(uncommon_ranges), 2):
        if str(self.text_box.index("sel.first")) == str(uncommon_ranges[i]):
            is_uncommon = True
            get_word_synonym(self, word)
            break

    try:
        # Add the replace word and ignore warning commands to the right-click menu
        if is_wrong:
            if self.replacement_word != "":
                word_menu.add_separator()
                word_menu.add_command(label=self.replacement_word, command=lambda: replace_word(self))
            word_menu.add_separator()
            word_menu.add_command(label="ignore warning", command=lambda: ignore_word(self, word))
        elif is_uncommon:
            if len(self.synonyms) > 0:
                word_menu.add_separator()
                word_menu.add_command(label=self.synonyms[1], command=lambda: replace_synonym(self))
            word_menu.add_separator()
            word_menu.add_command(label="ignore warning", command=lambda: ignore_word(self, word))
    except IndexError:
        print("Right click error")
    
    # Popup the right-click menu
    word_menu.tk_popup(event.x_root, event.y_root, 0)


# This function allows warning for the word to be ignored
def ignore_word(self, word):
    self.leaflet_master.ignore_words.append(word)
    check_spelling(self)


# This function gets the word replacement for the word
def get_word_replacement(self, word):
    text = Word(word)
    # Get the suggestion for the word and parse it
    suggestion = text.spellcheck()
    suggestion_text = suggestion[0]
    suggestion_text = str(suggestion_text).split(" ", 1)[0]
    suggestion_text = self.regex.sub('', suggestion_text)

    # Check if the suggestion is the same as the word, or if there are no suggestions
    if suggestion_text == "n" or suggestion_text == "":
        return False
    elif suggestion_text != word:
        self.replacement_word = suggestion_text
        return True
    else:
        return False


# This function gets the synonym for the word
def get_word_synonym(self, word):
    self.synonyms = []

    # Check if the word is in the ignore list, or if it is a common word
    if word in self.leaflet_master.common_words or word in self.leaflet_master.ignore_words \
            or word == "\n" or word.isspace() or len(word) == 1:
        return False
    # Get the synonym for the word
    else:
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                self.synonyms.append(lemma.name())
        return True


# This function replaces the word with the suggested word
def replace_word(self):
    self.text_box.delete("sel.first", "sel.last")
    self.text_box.insert("sel.first", self.replacement_word)
    check_spelling(self)


# This function replaces the word with the synonym
def replace_synonym(self):
    self.text_box.delete("sel.first", "sel.last")
    self.text_box.insert("sel.first", self.synonyms[1])
    self.leaflet_master.ignore_words.append(self.synonyms[1])


# This function copies the word to the clipboard
def copy_word(self):
    self.text_box.clipboard_clear()
    self.text_box.clipboard_append(self.text_box.selection_get())


# This function pastes the word from the clipboard
def paste_word(self):
    self.text_box.insert(tk.INSERT, self.text_box.clipboard_get())


# This function marks the word as bold, and makes it bold
def bold_word(self):
    ranges = self.text_box.tag_ranges("bold")
    mark = self.text_box.index("sel.first")
    if str(mark) in str(ranges):
        self.text_box.tag_remove("bold", "sel.first", "sel.last")
    else:
        self.text_box.tag_add("bold", "sel.first", "sel.last")
