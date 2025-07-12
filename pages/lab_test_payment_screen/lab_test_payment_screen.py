import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from datetime import datetime

class LabTestPaymentScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#EAF2F8')
        self.cart_data = None  # Initialize cart_data to None
        self.qr_code_icon = self._load_icon("fake_qr_code.png", (250, 250))

    def _load_icon(self, name, size):
        path = os.path.join("assets", "images", name)
        try:
            return ImageTk.PhotoImage(Image.open(path).resize(size, Image.LANCZOS))
        except FileNotFoundError:
            print(f"WARNING: QR code image '{name}' not found. Payment screen may not display it.")
            return None

    def on_show(self, data):
        """This method is called only when the frame is shown. It receives the cart data."""
        self.cart_data = data
        # Rebuild the UI with the new data when the frame is shown
        self.update_language()

    def update_language(self):
        """Rebuilds the UI with the current language. This method is now safe to call at any time."""
        for widget in self.winfo_children():
            widget.destroy()
        
        lang = self.controller.lang_manager

        tk.Label(self, text=lang.get('payment_method'), font=self.controller.title_font, bg='#EAF2F8').pack(pady=20)
        
        payment_method_frame = tk.Frame(self, bg='#EAF2F8')
        payment_method_frame.pack(pady=10)
        self.payment_var = tk.StringVar(value="Online")
        tk.Radiobutton(payment_method_frame, text=lang.get('online_payment'), variable=self.payment_var, value="Online", command=self.toggle_qr_code, font=("Helvetica", 12), bg='#EAF2F8').pack(side="left", padx=10)
        tk.Radiobutton(payment_method_frame, text=lang.get('cash_payment'), variable=self.payment_var, value="Cash", command=self.toggle_qr_code, font=("Helvetica", 12), bg='#EAF2F8').pack(side="left", padx=10)

        self.qr_frame = tk.Frame(self, bg='#EAF2F8')
        self.qr_frame.pack(pady=10)
        
        # THIS IS THE CRITICAL FIX:
        # We only build the payment details if cart_data actually exists. This prevents the crash.
        if self.cart_data:
            self.qr_label = tk.Label(self.qr_frame, image=self.qr_code_icon, bg='#EAF2F8')
            if self.qr_code_icon:
                self.qr_label.pack()
            
            total_text = lang.get('total_amount').format(amount=self.cart_data.get('total', 0))
            tk.Label(self.qr_frame, text=total_text, font=("Helvetica", 14, "bold"), bg='#EAF2F8').pack(pady=10)
            
            tk.Button(self, text=lang.get('confirm_payment_and_book'), command=self.confirm_and_save, font=self.controller.button_font, bg="#2ECC71", fg="white").pack(pady=20)
            self.toggle_qr_code()
        
        # Add a back button for navigation
        tk.Button(self, text=lang.get('back'), font=self.controller.button_font, command=lambda: self.controller.show_frame("LabTestSelectionScreen"), bg="#E74C3C", fg="white").pack(pady=10)

    def toggle_qr_code(self):
        if hasattr(self, 'qr_frame') and self.payment_var.get() == "Online":
            self.qr_frame.pack(pady=10)
        elif hasattr(self, 'qr_frame'):
            self.qr_frame.pack_forget()

    def confirm_and_save(self):
        payment_method = self.payment_var.get()
        status = "Online (Paid)" if payment_method == "Online" else "Cash (To be paid at counter)"
        save_lab_test_receipt(self.cart_data, status)
        
        lang = self.controller.lang_manager
        messagebox.showinfo(lang.get('booking_confirmed'), "Lab test booking is confirmed and a receipt has been saved.")
        self.controller.show_frame("WelcomeScreen")

def save_lab_test_receipt(cart_data, status):
    timestamp = datetime.now()
    date_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")

    items_html = "".join([f"<tr><td>{item['name']}</td><td>₹{item['price']}</td></tr>" for item in cart_data['items']])
    
    html_content = f"""
    <!DOCTYPE html><html><head><title>Lab Test Receipt</title>
    <style>body{{font-family:sans-serif;margin:20px;}}.container{{border:1px solid #ccc;padding:20px;width:600px;margin:auto;}}h1{{text-align:center;}}table{{width:100%;border-collapse:collapse;margin-top:20px;}}th,td{{border:1px solid #ddd;padding:8px;}}.total-row td{{font-weight:bold;}}.footer{{margin-top:20px;text-align:center;font-size:0.9em;color:#777;}}</style>
    </head><body><div class="container"><h1>Lab Test Receipt</h1><p><strong>Date:</strong> {date_str}</p>
    <table><thead><tr><th>Test/Package Name</th><th>Price</th></tr></thead><tbody>{items_html}</tbody></table>
    <table style="margin-top:0;"><tr class="total-row"><td>Total Amount</td><td style="text-align:right;">₹{cart_data['total']}</td></tr>
    <tr><td>Payment Status</td><td style="text-align:right;">{status}</td></tr></table>
    <div class="footer">Thank you for choosing our hospital.</div></div></body></html>
    """
    
    queue_folder = "lab_test_receipts"
    os.makedirs(queue_folder, exist_ok=True)
    
    file_timestamp = timestamp.strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(queue_folder, f"receipt_{file_timestamp}.html")
        
    try:
        with open(filename, 'w', encoding='utf-8') as f: f.write(html_content)
    except IOError as e:
        messagebox.showerror("Save Error", f"Could not save the receipt file.\nError: {e}")