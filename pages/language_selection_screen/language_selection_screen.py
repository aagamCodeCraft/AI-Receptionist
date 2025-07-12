import tkinter as tk
from tkinter import font as tkfont

class LanguageSelectionScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#EAF2F8')

        # Use a specific font that supports Hindi characters well
        self.hindi_font = tkfont.Font(family="Nirmala UI", size=14)

        title_label = tk.Label(self, text="Select Language / भाषा चुने", 
                               font=controller.title_font, bg='#EAF2F8', fg='#2C3E50')
        title_label.pack(pady=(80, 40))

        # --- English Button ---
        english_button = tk.Button(self, text="English",
                                   font=controller.button_font,
                                   command=lambda: self.select_language('en'),
                                   bg="#3498DB", fg="white", width=20, pady=10)
        english_button.pack(pady=10)

        # --- Hindi Button ---
        hindi_button = tk.Button(self, text="हिन्दी (Hindi)",
                                 font=self.hindi_font, # Use the special font for this button
                                 command=lambda: self.select_language('hi'),
                                 bg="#2ECC71", fg="white", width=20, pady=10)
        hindi_button.pack(pady=10)

    def select_language(self, lang_code):
        self.controller.set_language(lang_code)
        self.controller.show_frame("WelcomeScreen")