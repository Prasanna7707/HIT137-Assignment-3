import tkinter as tk
from tkinter import ttk
from func import fetch_query

class LanguageConverterBase:
    """ Base class providing basic attributes and methods for a language converter. """
    def __init__(self):
        self.languages = ["English", "French", "Spanish", "German", "Chinese","Hindi", "Nepali"]

    def fetch_translation(self, source_lang, target_lang, text):
        """ Translate text from source_lang to target_lang. """
        return fetch_query(source_lang, target_lang, text)

class TkinterGUI(tk.Tk, LanguageConverterBase):
    """ Main application class for the language converter using Tkinter. Inherits from tk.Tk and LanguageConverterBase. """
    def __init__(self):
        tk.Tk.__init__(self)
        LanguageConverterBase.__init__(self)
        self.title("Language Converter - HIT-137")
        self.geometry("450x250")
        self.configure(bg="#f0f0f0")  # Set background color

        style = ttk.Style(self)
        style.configure('TLabel', background='#FFD700', foreground='#007FFF', font=('Arial', 12))
        style.configure('TButton', font=('Arial Rounded MT Bold', 12, 'bold'), borderwidth='1', background='#32CD32')
        style.configure('TRadiobutton', background='#FF6347', foreground='white', font=('Arial', 10))
        style.configure('TEntry', font=('Arial', 12), foreground='#007FFF', borderwidth='5')
        style.configure('TCombobox', font=('Arial', 12), foreground='#007FFF', fieldbackground='#FFFFFF')
        style.map('TButton', background=[('active', '#FF69B4')])
        style.theme_use('clam')

        self.create_widgets()

    def create_widgets(self):
        """ Create and place widgets in the GUI """
        style = ttk.Style()
        style.configure("TLabel", background="#f0f0f0")  # Set label background color

        self.source_lang_label = ttk.Label(self, text="Source Language:")
        self.source_lang_label.grid(column=0, row=0, padx=10, pady=10, sticky="w")

        self.source_lang_combobox = ttk.Combobox(self, values=self.languages, width=20)
        self.source_lang_combobox.grid(column=1, row=0, padx=10, pady=10)
        self.source_lang_combobox.set("English")

        self.target_lang_label = ttk.Label(self, text="Target Language:")
        self.target_lang_label.grid(column=0, row=1, padx=10, pady=10, sticky="w")

        self.target_lang_combobox = ttk.Combobox(self, values=self.languages, width=20)
        self.target_lang_combobox.grid(column=1, row=1, padx=10, pady=10)
        self.target_lang_combobox.set("French")

        self.text_entry_label = ttk.Label(self, text="Text to translate:")
        self.text_entry_label.grid(column=0, row=2, padx=10, pady=10, sticky="w")

        self.text_entry = ttk.Entry(self, width=30)
        self.text_entry.grid(column=1, row=2, padx=10, pady=10)

        self.translate_button = ttk.Button(self, text="Translate", command=self.perform_translation)
        self.translate_button.grid(column=1, row=3, pady=10)

        self.result_label = ttk.Label(self, text="Translated text:", background="#f0f0f0")
        self.result_label.grid(column=0, row=4, padx=10, pady=10, sticky="w")

        self.result_text = ttk.Label(self, text="", wraplength=300)
        self.result_text.grid(column=1, row=4, padx=10, pady=10, sticky="w")

    def perform_translation(self):
        """ Fetch translation and update the result label. Demonstrates method overriding and polymorphism. """
        source_lang = self.source_lang_combobox.get()
        target_lang = self.target_lang_combobox.get()
        text_to_translate = self.text_entry.get()
        translation = self.fetch_translation(source_lang, target_lang, text_to_translate)
        self.result_text.config(text=translation)

# Run the application
if __name__ == "__main__":
    app = TkinterGUI()
    app.mainloop()