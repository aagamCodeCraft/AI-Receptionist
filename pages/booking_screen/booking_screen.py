import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import os
from datetime import datetime
import base64
# --- IMPORT THE SHARED SAVE FUNCTION ---
from pages.payment_screen.payment_screen import save_appointment_record

class BookingScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#EAF2F8')
        
        self.doctor_info = None
        self.captured_image = None
        self.image_path = None

        self.load_icons()

    def load_icons(self):
        self.back_icon = self._load_icon("back_arrow.png", (24, 24))
        self.home_icon = self._load_icon("home.png", (24, 24))

    def _load_icon(self, name, size):
        path = os.path.join("assets", "images", name)
        try: return ImageTk.PhotoImage(Image.open(path).resize(size, Image.LANCZOS))
        except FileNotFoundError: return None

    def on_show(self, data):
        self.doctor_info = data
        if self.image_path is None: # Don't reset if coming back from payment screen
            self.captured_image = None
        self.update_language()

    def update_language(self):
        if not self.doctor_info: return
        
        for widget in self.winfo_children():
            widget.destroy()

        lang = self.controller.lang_manager

        # Header and Form (mostly unchanged)
        header_frame = tk.Frame(self, bg='#EAF2F8'); header_frame.pack(side="top", fill="x", padx=10, pady=10)
        tk.Button(header_frame, image=self.back_icon, bg='#EAF2F8', relief="flat", command=lambda: self.controller.show_frame("DoctorSelectionScreen", self.doctor_info.get("specialty_key"))).pack(side="left")
        tk.Button(header_frame, image=self.home_icon, bg='#EAF2F8', relief="flat", command=lambda: self.controller.show_frame("WelcomeScreen")).pack(side="left", padx=5)
        self.title_label = tk.Label(header_frame, text=lang.get('booking_title'), font=self.controller.title_font, bg='#EAF2F8', fg='#2C3E50')
        self.title_label.pack(side="left", expand=True, fill="x")

        form_frame = tk.Frame(self, bg="white", padx=20, pady=20)
        form_frame.pack(pady=10, padx=20, fill="x")

        doctor_name_text = lang.get('booking_for').format(doctor_name=self.doctor_info['name'])
        tk.Label(form_frame, text=doctor_name_text, font=("Helvetica", 14, "bold"), bg="white").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))

        self.fields = {}
        form_config = {"patient_name": {"row": 1}, "phone_number": {"row": 2}, "age": {"row": 3}}
        for key, config in form_config.items():
            tk.Label(form_frame, text=lang.get(key), font=self.controller.button_font, bg="white").grid(row=config["row"], column=0, sticky="w", padx=5, pady=5)
            entry = tk.Entry(form_frame, font=self.controller.button_font, width=30)
            entry.grid(row=config["row"], column=1, sticky="w", padx=5, pady=5)
            self.fields[key] = entry
        
        # Gender Radio
        tk.Label(form_frame, text=lang.get('gender'), font=self.controller.button_font, bg="white").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.gender_var = tk.StringVar(value="Male")
        radio_frame = tk.Frame(form_frame, bg="white")
        tk.Radiobutton(radio_frame, text=lang.get('male'), variable=self.gender_var, value="Male", font=("Helvetica", 11), bg="white").pack(side="left")
        tk.Radiobutton(radio_frame, text=lang.get('female'), variable=self.gender_var, value="Female", font=("Helvetica", 11), bg="white").pack(side="left", padx=10)
        tk.Radiobutton(radio_frame, text=lang.get('other'), variable=self.gender_var, value="Other", font=("Helvetica", 11), bg="white").pack(side="left")
        radio_frame.grid(row=4, column=1, sticky="w", padx=5, pady=5)

        # Photo Capture
        photo_frame = tk.Frame(self, bg='#EAF2F8'); photo_frame.pack(pady=5)
        self.photo_canvas = tk.Canvas(photo_frame, width=128, height=128, bg="white", highlightthickness=1, highlightbackground="grey")
        self.photo_canvas.pack(side="left", padx=10)
        if self.captured_image: self.photo_canvas.create_image(0, 0, anchor="nw", image=self.photo_tk)
        
        self.capture_btn = tk.Button(photo_frame, text=lang.get('capture_photo'), command=self.capture_photo, font=self.controller.button_font)
        if self.image_path: self.capture_btn.config(text=lang.get('photo_captured'), state="disabled")
        self.capture_btn.pack(side="left", anchor="center")

        # --- NEW: Payment Method ---
        payment_frame = tk.Frame(self, bg="white", padx=20, pady=10)
        payment_frame.pack(pady=10, padx=20, fill="x")
        tk.Label(payment_frame, text=lang.get('payment_method'), font=self.controller.button_font, bg="white").pack(side="left", padx=5)
        self.payment_var = tk.StringVar(value="Online")
        tk.Radiobutton(payment_frame, text=lang.get('online_payment'), variable=self.payment_var, value="Online", font=("Helvetica", 11), bg="white").pack(side="left")
        tk.Radiobutton(payment_frame, text=lang.get('cash_payment'), variable=self.payment_var, value="Cash", font=("Helvetica", 11), bg="white").pack(side="left", padx=10)

        # --- UPDATED: Confirm Button ---
        self.confirm_btn = tk.Button(self, text=lang.get('proceed_to_payment'), command=self.process_booking, font=self.controller.button_font, bg="#2ECC71", fg="white", width=25, pady=8)
        self.confirm_btn.pack(pady=10)

    def capture_photo(self):
        # ... (This method is unchanged) ...
        lang = self.controller.lang_manager
        cap = cv2.VideoCapture(0)
        if not cap.isOpened(): messagebox.showerror("Camera Error", "Could not open webcam.") ; return
        cv2.namedWindow("Capture Photo - Press SPACE to save, ESC to exit")
        while True:
            ret, frame = cap.read()
            if not ret: break
            cv2.imshow("Capture Photo - Press SPACE to save, ESC to exit", frame)
            k = cv2.waitKey(1)
            if k % 256 == 27: break
            elif k % 256 == 32:
                if not os.path.exists("patient_photos"): os.makedirs("patient_photos")
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                self.image_path = f"patient_photos/patient_{timestamp}.png"
                cv2.imwrite(self.image_path, frame)
                self.captured_image = Image.open(self.image_path).resize((128, 128), Image.LANCZOS)
                self.photo_tk = ImageTk.PhotoImage(self.captured_image)
                self.photo_canvas.create_image(0, 0, anchor="nw", image=self.photo_tk)
                self.capture_btn.config(text=lang.get('photo_captured'), state="disabled")
                break
        cap.release()
        cv2.destroyAllWindows()

    def process_booking(self):
        """Validates form and directs to payment or saves directly."""
        # --- Validation ---
        patient_name = self.fields["patient_name"].get()
        phone_number = self.fields["phone_number"].get()
        age = self.fields["age"].get()
        if not all([patient_name, phone_number, age]):
            messagebox.showwarning("Incomplete Form", "Please fill out all the fields.")
            return
        if not self.image_path:
            messagebox.showwarning("Photo Required", "Please capture a photo of the patient.")
            return

        # --- Collect all data ---
        booking_data = {
            "patient_name": patient_name,
            "phone_number": phone_number,
            "age": age,
            "gender": self.gender_var.get(),
            "image_path": self.image_path,
            "doctor_info": self.doctor_info,
        }

        # --- Direct based on payment method ---
        payment_method = self.payment_var.get()
        if payment_method == "Online":
            self.controller.show_frame("PaymentScreen", booking_data)
        else: # Cash payment
            booking_data['payment_status'] = "Cash (To be paid at counter)"
            save_appointment_record(booking_data, self.controller)
            
            lang = self.controller.lang_manager
            messagebox.showinfo(lang.get('booking_confirmed'), f"Appointment with {self.doctor_info['name']} has been booked. Please pay at the counter.")
            self.controller.show_frame("WelcomeScreen")