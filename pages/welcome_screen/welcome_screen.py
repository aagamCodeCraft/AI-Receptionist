import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import simpleaudio as sa

class WelcomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#EAF2F8')
        self.load_icons()
        self.setup_widgets()

    def load_icons(self):
        icon_size = (32, 32)
        self.back_icon = self._load_icon("back_arrow.png", (24, 24))
        
        self.appointment_icon = self._load_icon("appointment.png", icon_size)
        self.emergency_icon = self._load_icon("emergency.png", icon_size)
        self.lab_test_icon = self._load_icon("lab_test.png", icon_size)
        self.existing_appointment_icon = self._load_icon("existing_appointment.png", icon_size)

    def _load_icon(self, name, size):
        path = os.path.join("assets", "images", name)
        try:
            return ImageTk.PhotoImage(Image.open(path).resize(size, Image.LANCZOS))
        except FileNotFoundError:
            print(f"Warning: Icon file not found at {path}")
            return None

    def setup_widgets(self):
        header_frame = tk.Frame(self, bg='#EAF2F8')
        header_frame.pack(side="top", fill="x", padx=10, pady=10)

        back_button = tk.Button(header_frame, image=self.back_icon, bg='#EAF2F8', relief="flat",
                                command=lambda: self.controller.show_frame("LanguageSelectionScreen"))
        if self.back_icon:
            back_button.image = self.back_icon
        back_button.pack(side="left")

        main_content_frame = tk.Frame(self, bg='#EAF2F8')
        main_content_frame.pack(expand=True)
        
        self.title_label = tk.Label(main_content_frame, font=self.controller.title_font, bg='#EAF2F8', fg='#2C3E50')
        self.title_label.pack(side="top", fill="x", pady=(0, 20))

        button_font = self.controller.button_font
        
        self.buttons_config = {
            "book_appointment": {"icon": self.appointment_icon, "command": lambda: self.controller.show_frame("SpecialtySelectionScreen")},
            "emergency": {"icon": self.emergency_icon, "command": self.trigger_emergency_alarm},
            # --- THIS IS THE FIX: Changed "LabTestScreen" to "LabTestSelectionScreen" ---
            "lab_test": {"icon": self.lab_test_icon, "command": lambda: self.controller.show_frame("LabTestSelectionScreen")},
            "existing_appointment": {"icon": self.existing_appointment_icon, "command": lambda: self.controller.show_frame("ExistingAppointmentScreen")}
        }
        
        self.buttons = {}
        for key, config in self.buttons_config.items():
            btn = tk.Button(main_content_frame, image=config["icon"], compound="left", font=button_font,
                             command=config["command"], fg="white",
                             width=250, height=50, padx=15, relief="flat")
            if config["icon"]:
                btn.image = config["icon"]
            btn.pack(pady=8)
            self.buttons[key] = btn
        
        self.buttons["book_appointment"].config(bg="#3498DB")
        self.buttons["emergency"].config(bg="#E74C3C")
        self.buttons["lab_test"].config(bg="#2ECC71")
        self.buttons["existing_appointment"].config(bg="#F1C40F")

        self.update_language()

    def trigger_emergency_alarm(self):
        sound_path = os.path.join("assets", "sounds", "emergency_alarm.wav")
        if not os.path.exists(sound_path):
            messagebox.showerror("Error", f"Emergency sound file not found at {os.path.abspath(sound_path)}")
            return
        try:
            wave_obj = sa.WaveObject.from_wave_file(sound_path)
            wave_obj.play()
            messagebox.showinfo("Emergency", "Help is on the way! An alarm has been sounded.")
        except Exception as e:
            messagebox.showerror("Sound Error", f"Could not play the alarm sound.\nError: {e}")

    def update_language(self):
        lang = self.controller.lang_manager
        self.title_label.config(text=lang.get("welcome_title"))
        for key, button in self.buttons.items():
            button.config(text=lang.get(key))