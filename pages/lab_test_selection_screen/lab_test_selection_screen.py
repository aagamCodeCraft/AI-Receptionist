import tkinter as tk
from tkinter import messagebox

class LabTestSelectionScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#EAF2F8')

        # Prices are defined by a key. The display name comes from the language file.
        self.packages_prices = {
            "basic_health_check": 500,
            "full_body_checkup": 1500,
            "senior_citizen_profile": 1200,
            "diabetic_profile": 900,
            "womens_wellness": 2000
        }
        self.individual_tests_prices = {
            "blood_sugar_test": 150,
            "lipid_profile": 350,
            "thyroid_function_test": 400,
            "liver_function_test": 300,
            "complete_blood_count": 250,
            "kidney_function_test": 300,
            "vitamin_d_test": 800,
            "urine_analysis": 100
        }
        
        # Will be populated by update_language
        self.package_vars = {}
        self.test_vars = {}
        
        self.setup_widgets()
        self.update_language()

    def setup_widgets(self):
        # Clear any existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        self.main_frame = tk.Frame(self, bg='#EAF2F8')
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.title_label = tk.Label(self.main_frame, font=self.controller.title_font, bg='#EAF2F8')
        self.title_label.pack(pady=(0, 20))

        # Packages Frame
        self.packages_frame = tk.LabelFrame(self.main_frame, font=("Helvetica", 14, "bold"), bg='#EAF2F8', bd=2, relief="groove")
        self.packages_frame.pack(fill="x", pady=10)

        # Individual Tests Frame
        self.tests_frame = tk.LabelFrame(self.main_frame, font=("Helvetica", 14, "bold"), bg='#EAF2F8', bd=2, relief="groove")
        self.tests_frame.pack(fill="x", pady=10)
            
        # Bottom navigation
        self.bottom_frame = tk.Frame(self.main_frame, bg='#EAF2F8')
        self.bottom_frame.pack(fill='x', side='bottom', pady=10)

        self.back_button = tk.Button(self.bottom_frame, font=self.controller.button_font, command=lambda: self.controller.show_frame("WelcomeScreen"), bg="#E74C3C", fg="white")
        self.back_button.pack(side="left")
        
        self.cart_button = tk.Button(self.bottom_frame, font=self.controller.button_font, command=self.view_cart_popup, bg="#3498DB", fg="white")
        self.cart_button.pack(side="right")

    def get_selected_items(self):
        selected = {}
        lang = self.controller.lang_manager
        # Get translated names for packages
        package_names = lang.get("lab_tests")["packages"]
        for key, var in self.package_vars.items():
            if var.get():
                display_name = package_names.get(key, key)
                selected[display_name] = self.packages_prices[key]
        
        # Get translated names for individual tests
        test_names = lang.get("lab_tests")["individual"]
        for key, var in self.test_vars.items():
            if var.get():
                display_name = test_names.get(key, key)
                selected[display_name] = self.individual_tests_prices[key]
        return selected

    def view_cart_popup(self):
        selected_items = self.get_selected_items()
        lang = self.controller.lang_manager
        
        if not selected_items:
            messagebox.showinfo(lang.get('cart_summary'), lang.get('no_tests_selected'))
            return

        total_price = sum(selected_items.values())
        cart_details = "\n".join([f"- {name} (₹{price})" for name, price in selected_items.items()])
        popup_text = f"{lang.get('selected_items')}:\n{cart_details}\n\n{lang.get('total')}: ₹{total_price}"
        
        if messagebox.askokcancel(lang.get('cart_summary'), popup_text + f"\n\n{lang.get('proceed_to_payment')}?"):
            # Pass original keys and prices to payment screen
            cart_data_items = [{'name': name, 'price': price} for name, price in selected_items.items()]
            cart_data = {'items': cart_data_items, 'total': total_price}
            self.controller.show_frame("LabTestPaymentScreen", data=cart_data)

    def update_language(self):
        lang = self.controller.lang_manager
        
        # Update titles
        self.title_label.config(text=lang.get('lab_test_title'))
        self.packages_frame.config(text=lang.get('packages_and_offers'))
        self.tests_frame.config(text=lang.get('individual_tests'))
        self.back_button.config(text=lang.get('back'))
        
        # Update cart button text
        selected_count = len(self.get_selected_items())
        self.cart_button.config(text=lang.get('view_cart').format(count=selected_count))
        
        # --- Recreate Checkbuttons with translated text ---
        for widget in self.packages_frame.winfo_children(): widget.destroy()
        for widget in self.tests_frame.winfo_children(): widget.destroy()

        package_names = lang.get("lab_tests")["packages"]
        self.package_vars = {key: tk.BooleanVar() for key in self.packages_prices}
        for key, price in self.packages_prices.items():
            display_name = package_names.get(key, key)
            tk.Checkbutton(self.packages_frame, text=f"{display_name} - ₹{price}", variable=self.package_vars[key], font=("Helvetica", 12), bg='#EAF2F8').pack(anchor="w", padx=10)

        test_names = lang.get("lab_tests")["individual"]
        self.test_vars = {key: tk.BooleanVar() for key in self.individual_tests_prices}
        for key, price in self.individual_tests_prices.items():
            display_name = test_names.get(key, key)
            tk.Checkbutton(self.tests_frame, text=f"{display_name} - ₹{price}", variable=self.test_vars[key], font=("Helvetica", 12), bg='#EAF2F8').pack(anchor="w", padx=10)