import tkinter as tk

from textblob import Word
from nltk.corpus import wordnet


def word_complexity_check(self):
    for word in self.text.split(' '):
        word_positions = [i for i in range(len(self.text)) if self.text.startswith(word, i)]
        word = self.regex.sub('', word)
        for position in word_positions:
            if word in self.leaflet_master.common_words or word in self.leaflet_master.ignore_uncommon_words:
                self.text_box.tag_remove("uncommon", f'1.{position}', f'1.{position + len(word)}')
            elif position in self.misspelled_tag:
                self.text_box.tag_remove("uncommon", f'1.{position}', f'1.{position + len(word)}')
            else:
                self.text_box.tag_add("uncommon", f'1.{position}', f'1.{position + len(word)}')


def check_spelling(self):
    self.text = self.text_box.get("1.0", tk.END)
    current_spaces = self.text.count(' ')
    self.misspelled_tag = []
    if current_spaces != self.num_spaces:
        self.num_spaces = current_spaces
        for word in self.text.split(' '):
            word_positions = [i for i in range(len(self.text)) if self.text.startswith(word, i)]
            suggestion = Word.spellcheck(Word(word))
            suggestion_text = suggestion[0]
            suggestion_text = str(suggestion_text).split(" ", 1)[0]
            suggestion_text = self.regex.sub('', suggestion_text)
            word = self.regex.sub('', word)
            for position in word_positions:
                self.misspelled_tag.append(position)
                if suggestion_text != word and suggestion_text != "n":
                    self.text_box.tag_add("wrong", f'1.{position}', f'1.{position + len(word)}')
                else:
                    self.text_box.tag_remove("wrong", f'1.{position}', f'1.{position + len(word)}')
                    self.misspelled_tag.remove(position)
        word_complexity_check(self)


def word_right_click(self, event):
    word = self.text_box.get("@%d,%d wordstart" % (event.x, event.y), "@%d,%d wordend" % (event.x, event.y))
    self.text_box.mark_set("insert", "@%d,%d" % (event.x, event.y))
    self.text_box.mark_set("sel.first", "insert wordstart")
    self.text_box.mark_set("sel.last", "insert wordend")
    word_menu = tk.Menu(self.master, tearoff=0)
    word_menu.add_command(label="Copy", command=self.copy_word)
    word_menu.add_command(label="Paste", command=self.paste_word)
    is_wrong = get_word_replacement(self, word)
    is_uncommon = get_word_synonym(self, word)
    if is_wrong:
        word_menu.add_separator()
        word_menu.add_command(label=self.replacement_word, command=self.replace_word)
    elif is_uncommon:
        word_menu.add_separator()
        word_menu.add_command(label=self.synonyms[1], command=self.replace_synonym)
        word_menu.add_separator()
        word_menu.add_command(label="ignore", command=self.leaflet_master.ignore_uncommon_words.append(word))
    word_menu.tk_popup(event.x_root, event.y_root, 0)


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
    if word in self.leaflet_master.common_words or word in self.leaflet_master.ignore_uncommon_words or word == "\n" or word.isspace():
        return False
    else:
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                self.synonyms.append(lemma.name())
        return True


def replace_word(self):
    self.text_box.delete("sel.first", "sel.last")
    self.text_box.insert("sel.first", self.replacement_word)
    word_complexity_check(self)


def replace_synonym(self):
    self.text_box.delete("sel.first", "sel.last")
    self.text_box.insert("sel.first", self.synonyms[1])
    self.leaflet_master.ignore_uncommon_words.append(self.synonyms[1])


def copy_word(self):
    self.text_box.clipboard_clear()
    self.text_box.clipboard_append(self.text_box.selection_get())


def paste_word(self):
    self.text_box.insert(tk.INSERT, self.text_box.clipboard_get())
