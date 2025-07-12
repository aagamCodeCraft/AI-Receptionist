import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk
import os
from data.hospital_data import DOCTORS

class DoctorSelectionScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#EAF2F8')
        self.current_specialty = None
        self.load_all_icons()

    def load_all_icons(self):
        self.back_icon = self._load_icon("back_arrow.png", (24, 24))
        self.home_icon = self._load_icon("home.png", (24, 24))
        self.doctor_icons = {
            "doctor_male.png": self._load_icon("doctor_male.png", (100, 100)),
            "doctor_female.png": self._load_icon("doctor_female.png", (100, 100))
        }
        self.detail_icons = {
            "email": self._load_icon("email.png", (20, 20)),
            "timings": self._load_icon("clock.png", (20, 20)),
            "holidays": self._load_icon("calendar.png", (20, 20)),
            "fees": self._load_icon("dollar.png", (20, 20))
        }

    def _load_icon(self, name, size):
        path = os.path.join("assets", "images", name)
        try:
            return ImageTk.PhotoImage(Image.open(path).resize(size, Image.LANCZOS))
        except FileNotFoundError:
            print(f"Icon not found: {name}")
            return None

    def on_show(self, specialty_key):
        self.current_specialty = specialty_key
        self.update_language()

    def update_language(self):
        if not self.current_specialty: return
        for widget in self.winfo_children(): widget.destroy()
        
        lang = self.controller.lang_manager
        translated_specialty = lang.get('specialties').get(self.current_specialty, self.current_specialty)
        
        header_frame = tk.Frame(self, bg='#EAF2F8'); header_frame.pack(side="top", fill="x", padx=10, pady=10)
        tk.Button(header_frame, image=self.back_icon, bg='#EAF2F8', relief="flat", command=lambda: self.controller.show_frame("SpecialtySelectionScreen")).pack(side="left")
        tk.Button(header_frame, image=self.home_icon, bg='#EAF2F8', relief="flat", command=lambda: self.controller.show_frame("WelcomeScreen")).pack(side="left", padx=5)
        
        title_text = f"{lang.get('doctors_for')} {translated_specialty}"
        tk.Label(header_frame, text=title_text, font=self.controller.title_font, bg='#EAF2F8', fg='#2C3E50').pack(side="left", expand=True, fill="x")
        
        canvas = tk.Canvas(self, bg='#EAF2F8', highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#EAF2F8')
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=5)
        scrollbar.pack(side="right", fill="y", padx=(0, 20))
        
        doctors = DOCTORS.get(self.current_specialty, [])
        for doctor in doctors:
            self.create_doctor_profile(scrollable_frame, doctor)

    def create_doctor_profile(self, parent, doctor_info):
        lang = self.controller.lang_manager
        
        is_hindi = lang.current_lang == "hi"
        doctor_name = doctor_info.get("name_hi") if is_hindi else doctor_info.get("name")
        doctor_details = doctor_info.get("details_hi") if is_hindi else doctor_info.get("details")
        
        frame = tk.Frame(parent, borderwidth=1, relief="solid", padx=15, pady=15, bg="white"); frame.pack(fill="x", pady=10)
        frame.grid_columnconfigure(1, weight=1)

        photo = self.doctor_icons.get(doctor_info["photo"]); photo_label = tk.Label(frame, image=photo, bg="white")
        if photo: photo_label.image = photo
        photo_label.grid(row=0, column=0, rowspan=6, sticky="nw", padx=(0, 15))

        tk.Label(frame, text=doctor_name, font=("Helvetica", 16, "bold"), bg="white", anchor="w").grid(row=0, column=1, sticky="w")
        tk.Label(frame, text=doctor_details, font=("Helvetica", 11), bg="white", anchor="w", justify="left").grid(row=1, column=1, sticky="w", pady=(0, 10))
        
        availability_text = lang.get(doctor_info["availability"].lower())
        status_color = "#2ECC71" if doctor_info["availability"] == "Available" else "#E74C3C"
        tk.Label(frame, text=f"● {availability_text}", font=("Helvetica", 12, "bold"), bg="white", fg=status_color, anchor="w").grid(row=0, column=2, sticky="ne")

        def create_detail_row(icon_key, text, row):
            icon_label = tk.Label(frame, image=self.detail_icons.get(icon_key), bg="white")
            if self.detail_icons.get(icon_key): icon_label.image = self.detail_icons.get(icon_key)
            icon_label.grid(row=row, column=1, sticky="w", padx=(0, 5))
            tk.Label(frame, text=text, font=("Helvetica", 11), bg="white", anchor="w").grid(row=row, column=1, sticky="w", padx=(25, 0))

        # --- TIMINGS TRANSLATION LOGIC (CORRECTED) ---
        timings_text = doctor_info.get("timings", "")
        weekday_translations = lang.get("weekdays")
        if is_hindi and isinstance(weekday_translations, dict):
            # Create a temporary copy to avoid modifying the original
            temp_timings_text = timings_text
            for key, value in weekday_translations.items():
                # Replace title-cased English abbreviation (e.g., "Mon") with Hindi translation
                temp_timings_text = temp_timings_text.replace(key.title(), value)
            timings_text = temp_timings_text

        create_detail_row("email", doctor_info["email"], 2)
        create_detail_row("timings", timings_text, 3)
        create_detail_row("fees", lang.get("consultation_fee").format(fees=doctor_info["fees"]), 4)
        
        # Ensure weekday_translations is a dictionary before proceeding
        if isinstance(weekday_translations, dict):
            translated_holidays = ", ".join([weekday_translations.get(day, day.upper()) for day in doctor_info.get("holidays", [])])
        else:
            translated_holidays = ", ".join(doctor_info.get("holidays", [])).upper()

        holidays_text = lang.get("holidays").format(holidays=translated_holidays)
        create_detail_row("holidays", holidays_text, 5)
        
        doctor_info_with_specialty = doctor_info.copy()
        doctor_info_with_specialty["specialty_key"] = self.current_specialty
        
        book_button = tk.Button(frame, text=lang.get("book_now"), 
                                command=lambda d=doctor_info_with_specialty: self.controller.show_frame("BookingScreen", d),
                                bg="#DC3545", fg="white", font=("Helvetica", 12, "bold"), relief="flat", padx=10, pady=5)
        book_button.grid(row=1, column=2, rowspan=2, sticky="se", padx=5, pady=5)
        if doctor_info["availability"] == "Unavailable":
            book_button.config(state="disabled", bg="grey")