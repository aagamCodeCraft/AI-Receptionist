import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import base64
from datetime import datetime

class PaymentScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#EAF2F8')
        self.booking_data = None
        
        self.load_icons()

    def load_icons(self):
        self.back_icon = self._load_icon("back_arrow.png", (24, 24))
        self.home_icon = self._load_icon("home.png", (24, 24))
        self.qr_code_icon = self._load_icon("fake_qr_code.png", (250, 250))

    def _load_icon(self, name, size):
        path = os.path.join("assets", "images", name)
        try:
            return ImageTk.PhotoImage(Image.open(path).resize(size, Image.LANCZOS))
        except FileNotFoundError:
            print(f"Warning: Icon '{name}' not found at '{path}'")
            return None

    def on_show(self, data):
        self.booking_data = data
        self.update_language()

    def update_language(self):
        if not self.booking_data: return
        
        for widget in self.winfo_children():
            widget.destroy()

        lang = self.controller.lang_manager

        # --- Header ---
        header_frame = tk.Frame(self, bg='#EAF2F8')
        header_frame.pack(side="top", fill="x", padx=10, pady=10)
        tk.Button(header_frame, image=self.back_icon, bg='#EAF2F8', relief="flat", command=lambda: self.controller.show_frame("BookingScreen", self.booking_data["doctor_info"])).pack(side="left")
        tk.Button(header_frame, image=self.home_icon, bg='#EAF2F8', relief="flat", command=lambda: self.controller.show_frame("WelcomeScreen")).pack(side="left", padx=5)
        
        # --- Content ---
        tk.Label(self, text=lang.get('scan_to_pay'), font=self.controller.title_font, bg='#EAF2F8', fg='#2C3E50').pack(pady=20)
        
        qr_label = tk.Label(self, image=self.qr_code_icon, bg='#EAF2F8')
        qr_label.pack(pady=10)
        
        fees = self.booking_data["doctor_info"]["fees"]
        tk.Label(self, text=f"{lang.get('consultation_fee').format(fees=fees)}", font=("Helvetica", 14, "bold"), bg='#EAF2F8').pack(pady=10)

        # --- Confirm Button ---
        confirm_btn = tk.Button(self, text=lang.get('confirm_payment_and_book'), command=self.confirm_and_save, font=self.controller.button_font, bg="#2ECC71", fg="white", width=30, pady=8)
        confirm_btn.pack(pady=20)

    def confirm_and_save(self):
        """Saves the final record after 'payment'."""
        self.booking_data['payment_status'] = "Online (Paid)"
        save_appointment_record(self.booking_data, self.controller)
        
        lang = self.controller.lang_manager
        messagebox.showinfo(lang.get('booking_confirmed'), f"Appointment with {self.booking_data['doctor_info']['name']} has been booked and a printable record has been saved.")
        self.controller.show_frame("WelcomeScreen")

# This is a shared function that can be called from anywhere to save the record
def save_appointment_record(booking_data, controller):
    """Creates a self-contained HTML file for the appointment."""
    # ... (The HTML generation logic is now here) ...
    patient_name = booking_data['patient_name']
    image_path = booking_data['image_path']
    timestamp = datetime.now()
    appointment_date_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")

    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    except IOError as e:
        messagebox.showerror("Image Error", f"Could not read the captured photo file.\nError: {e}")
        return
        
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Patient Appointment: {patient_name}</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 20px; color: #333; }}
            .container {{ max-width: 800px; margin: auto; border: 2px solid #007BFF; padding: 20px; border-radius: 10px; background-color: #f9f9f9; }}
            h1 {{ color: #0056b3; text-align: center; border-bottom: 2px solid #007BFF; padding-bottom: 10px; }}
            .main-content {{ display: flex; align-items: flex-start; margin-top: 20px; }}
            .patient-photo {{ margin-right: 30px; border: 2px solid #ccc; padding: 5px; border-radius: 5px; }}
            .patient-photo img {{ width: 200px; height: auto; }}
            .details-table {{ flex-grow: 1; border-collapse: collapse; width: 100%; }}
            .details-table th, .details-table td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            .details-table th {{ background-color: #e9ecef; width: 30%; }}
            .payment-status {{ font-weight: bold; color: {'green' if booking_data['payment_status'].startswith('Online') else 'orange'}; }}
            .footer {{ text-align: center; margin-top: 20px; font-size: 0.9em; color: #777; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Hospital Appointment Record</h1>
            <div class="main-content">
                <div class="patient-photo">
                    <img src="data:image/png;base64,{encoded_string}" alt="Patient Photo">
                </div>
                <table class="details-table">
                    <tr><th colspan="2" style="background-color: #007BFF; color: white; text-align: center;">PATIENT & APPOINTMENT DETAILS</th></tr>
                    <tr><th>Patient Name</th><td>{booking_data['patient_name']}</td></tr>
                    <tr><th>Phone Number</th><td>{booking_data['phone_number']}</td></tr>
                    <tr><th>Age</th><td>{booking_data['age']}</td></tr>
                    <tr><th>Gender</th><td>{booking_data['gender']}</td></tr>
                    <tr><th style="height: 20px;" colspan="2"></th></tr>
                    <tr><th>Doctor</th><td>{booking_data['doctor_info']['name']}</td></tr>
                    <tr><th>Specialty</th><td>{controller.lang_manager.get_specialty(booking_data['doctor_info']['specialty_key'])}</td></tr>
                    <tr><th>Consultation Fee</th><td>{booking_data['doctor_info']['fees']}</td></tr>
                    <tr><th>Payment Status</th><td class="payment-status">{booking_data['payment_status']}</td></tr>
                </table>
            </div>
            <div class="footer">
                Appointment booked by: aagamCodeCraft on {appointment_date_str}
            </div>
        </div>
    </body>
    </html>
    """
        
    queue_folder = "patient_appointment_queue"
    if not os.path.exists(queue_folder):
        os.makedirs(queue_folder)
            
    safe_patient_name = "".join(c for c in patient_name if c.isalnum() or c in (' ', '_')).rstrip()
    file_timestamp = timestamp.strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(queue_folder, f"{safe_patient_name.replace(' ', '_')}_{file_timestamp}.html")
        
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
    except IOError as e:
        messagebox.showerror("Save Error", f"Could not save the appointment file.\nError: {e}")