import tkinter as tk
from tkinter import font as tkfont

from utils.language_manager import LanguageManager
from pages.language_selection_screen.language_selection_screen import LanguageSelectionScreen
from pages.welcome_screen.welcome_screen import WelcomeScreen
from pages.specialty_selection_screen.specialty_selection_screen import SpecialtySelectionScreen
from pages.doctor_selection_screen.doctor_selection_screen import DoctorSelectionScreen
from pages.booking_screen.booking_screen import BookingScreen
from pages.payment_screen.payment_screen import PaymentScreen
from pages.lab_test_selection_screen.lab_test_selection_screen import LabTestSelectionScreen
from pages.lab_test_payment_screen.lab_test_payment_screen import LabTestPaymentScreen
# --- ADDED: Import the new screen ---
from pages.existing_appointment_screen.existing_appointment_screen import ExistingAppointmentScreen

class AIReceptionist(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("AI Receptionist")
        self.geometry("700x600")

        self.lang_manager = LanguageManager()
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold")
        self.button_font = tkfont.Font(family='Helvetica', size=12)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        # --- UPDATED: Added the new screen to the frame loop ---
        for F in (LanguageSelectionScreen, WelcomeScreen, SpecialtySelectionScreen, 
                  DoctorSelectionScreen, BookingScreen, PaymentScreen,
                  LabTestSelectionScreen, LabTestPaymentScreen, ExistingAppointmentScreen):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.update_all_frames_language()
        self.show_frame("LanguageSelectionScreen")

    def show_frame(self, page_name, data=None):
        frame = self.frames[page_name]
        if hasattr(frame, "on_show"):
            frame.on_show(data)
        
        if hasattr(frame, "update_language"):
            frame.update_language()
            
        frame.tkraise()

    def set_language(self, lang_code):
        self.lang_manager.load_language(lang_code)
        self.update_all_frames_language()

    def update_all_frames_language(self):
        for frame in self.frames.values():
            if hasattr(frame, "update_language"):
                frame.update_language()

if __name__ == "__main__":
    app = AIReceptionist()
    app.mainloop()