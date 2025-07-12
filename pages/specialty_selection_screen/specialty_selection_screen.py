import tkinter as tk
from PIL import Image, ImageTk
import os

class SpecialtySelectionScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#EAF2F8')

        # Store widgets that need text updates
        self.title_label = None
        self.buttons_frame = None
        self.specialty_keys = [
            "Cardiology", "Orthopedics", "Dermatology", 
            "Neurology", "Gynecology", "General Physician"
        ]

        self.load_icons()
        self.update_language() # Draw UI with initial language

    def load_icons(self):
        self.back_icon = self._load_icon("back_arrow.png", (24, 24))
        self.home_icon = self._load_icon("home.png", (24, 24))
        self.specialty_icons = {
            "Cardiology": self._load_icon("cardiology.png", (64, 64)),
            "Orthopedics": self._load_icon("orthopedics.png", (64, 64)),
            "Dermatology": self._load_icon("dermatology.png", (64, 64)),
            "Neurology": self._load_icon("neurology.png", (64, 64)),
            "Gynecology": self._load_icon("gynecology.png", (64, 64)),
            "General Physician": self._load_icon("general_physician.png", (64, 64))
        }

    def _load_icon(self, name, size):
        path = os.path.join("assets", "images", name)
        try: return ImageTk.PhotoImage(Image.open(path).resize(size, Image.LANCZOS))
        except FileNotFoundError: return None

    def update_language(self):
        """Redraws the entire UI with the new language."""
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()
        
        lang = self.controller.lang_manager
        
        # Header
        header_frame = tk.Frame(self, bg='#EAF2F8')
        header_frame.pack(side="top", fill="x", padx=10, pady=10)
        
        tk.Button(header_frame, image=self.back_icon, bg='#EAF2F8', relief="flat", command=lambda: self.controller.show_frame("WelcomeScreen")).pack(side="left")
        tk.Button(header_frame, image=self.home_icon, bg='#EAF2F8', relief="flat", command=lambda: self.controller.show_frame("WelcomeScreen")).pack(side="left", padx=5)

        self.title_label = tk.Label(header_frame, text=lang.get("choose_specialty"), font=self.controller.title_font, bg='#EAF2F8', fg='#2C3E50')
        self.title_label.pack(side="left", expand=True, fill="x")

        # Buttons Grid
        self.buttons_frame = tk.Frame(self, bg='#EAF2F8')
        self.buttons_frame.pack(expand=True, fill="both", padx=20, pady=10)

        row, col = 0, 0
        for key in self.specialty_keys:
            icon = self.specialty_icons.get(key)
            # Pass original key to the command, get translated text for display
            translated_text = lang.get_specialty(key)
            btn = tk.Button(self.buttons_frame, text=translated_text, image=icon, compound="top", font=self.controller.button_font,
                            relief="flat", bg="white", fg="#2C3E50", pady=10,
                            command=lambda s=key: self.controller.show_frame("DoctorSelectionScreen", s))
            btn.image = icon
            btn.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            
            col += 1
            if col > 1: col = 0; row += 1
        
        for i in range(2): self.buttons_frame.grid_columnconfigure(i, weight=1)
        for i in range(row + 1): self.buttons_frame.grid_rowconfigure(i, weight=1)