# Import necessary libraries and modules
import tkinter as tk

from textblob import Word
from nltk.corpus import wordnet
import re


def check_spelling(self):
    self.text = self.text_box.get("1.0", tk.END)
    current_spaces = self.text.count(' ')
    self.misspelled_tag = []
    if current_spaces != self.num_spaces:
        self.num_spaces = current_spaces
        for word in self.text.split(' '):
            word = word.lower()
            word_positions = [word_start for word_start in range(len(self.text)-len(word)+1) if self.text[word_start:word_start+len(word)] == word]
            suggestion = Word.spellcheck(Word(word))
            suggestion_text = suggestion[0]
            suggestion_text = str(suggestion_text).split(" ", 1)[0]
            suggestion_text = self.regex.sub('', suggestion_text)
            word = re.sub(r'[.;:,?"!/]', '', word)
            word_parsed = self.regex.sub('', word)
            for position in word_positions:
                self.misspelled_tag.append(position)
                word_found = find_word_in_list(suggestion, word_parsed)
                if suggestion_text != "n" and word_found is False and word_parsed != "\n" and word_parsed.isspace() is False and len(word_parsed) \
                        != 1 and word not in self.leaflet_master.ignore_words and word != "-":
                    self.text_box.tag_add("wrong", f'1.{position}', f'1.{position + len(word)}')
                else:
                    self.text_box.tag_remove("wrong", f'1.{position}', f'1.{position + len(word)}')
                    self.misspelled_tag.remove(position)
        word_complexity_check(self)


def word_complexity_check(self):
    for word in self.text.split(' '):
        word_positions = [word_start for word_start in range(len(self.text)-len(word)+1) if self.text[word_start:word_start+len(word)] == word]
        word = word.lower()
        word = re.sub(r'[.;:,?"!/]', '', word)
        word_parsed = self.regex.sub('', word)
        for position in word_positions:
            if get_word_synonym(self, word_parsed) and len(self.synonyms) == 0 and word not in self.leaflet_master.ignore_words and word != "-":
                self.text_box.tag_remove("uncommon", f'1.{position}', f'1.{position + len(word)}')
                self.text_box.tag_add("wrong", f'1.{position}', f'1.{position + len(word)}')
                self.misspelled_tag.append(position)
            elif word_parsed in self.leaflet_master.common_words or word in self.leaflet_master.ignore_words or position in self.misspelled_tag:
                self.text_box.tag_remove("uncommon", f'1.{position}', f'1.{position + len(word)}')
            else:
                self.text_box.tag_add("uncommon", f'1.{position}', f'1.{position + len(word)}')


def find_word_in_list(suggestion, word):
    for suggestionWord in suggestion:
        if word == suggestionWord[0]:
            return True
    return False


def word_right_click(self, event):
    word = self.text_box.get("@%d,%d wordstart" % (event.x, event.y), "@%d,%d wordend" % (event.x, event.y))
    self.text_box.mark_set("insert", "@%d,%d" % (event.x, event.y))
    self.text_box.mark_set("sel.first", "insert wordstart")
    self.text_box.mark_set("sel.last", "insert wordend")
    wrong_ranges = self.text_box.tag_ranges("wrong")
    uncommon_ranges = self.text_box.tag_ranges("uncommon")
    word_menu = tk.Menu(self.master, tearoff=0)
    word_menu.add_command(label="Copy", command=lambda: copy_word(self))
    word_menu.add_command(label="Paste", command=lambda: paste_word(self))
    word_menu.add_command(label="Bold", command=lambda: bold_word(self))
    is_wrong = False
    is_uncommon = False

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
    word_menu.tk_popup(event.x_root, event.y_root, 0)


def ignore_word(self, word):
    self.leaflet_master.ignore_words.append(word)
    check_spelling(self)


def get_word_replacement(self, word):
    text = Word(word)
    suggestion = text.spellcheck()
    suggestion_text = suggestion[0]
    suggestion_text = str(suggestion_text).split(" ", 1)[0]
    suggestion_text = self.regex.sub('', suggestion_text)
    if suggestion_text == "n" or suggestion_text == "":
        return False
    elif suggestion_text != word:
        self.replacement_word = suggestion_text
        return True
    else:
        return False


def get_word_synonym(self, word):
    self.synonyms = []
    if word in self.leaflet_master.common_words or word in self.leaflet_master.ignore_words \
            or word == "\n" or word.isspace() or len(word) == 1:
        return False
    else:
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                self.synonyms.append(lemma.name())
        return True


def replace_word(self):
    self.text_box.delete("sel.first", "sel.last")
    self.text_box.insert("sel.first", self.replacement_word)
    check_spelling(self)


def replace_synonym(self):
    self.text_box.delete("sel.first", "sel.last")
    self.text_box.insert("sel.first", self.synonyms[1])
    self.leaflet_master.ignore_words.append(self.synonyms[1])


def copy_word(self):
    self.text_box.clipboard_clear()
    self.text_box.clipboard_append(self.text_box.selection_get())


def paste_word(self):
    self.text_box.insert(tk.INSERT, self.text_box.clipboard_get())


def bold_word(self):
    ranges = self.text_box.tag_ranges("bold")
    mark = self.text_box.index("sel.first")
    if str(mark) in str(ranges):
        self.text_box.tag_remove("bold", "sel.first", "sel.last")
    else:
        self.text_box.tag_add("bold", "sel.first", "sel.last")
