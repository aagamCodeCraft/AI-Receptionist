import tkinter as tk
from tkinter import messagebox
from data.hospital_data import ALL_DOCTORS

class ExistingAppointmentScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#EAF2F8')
        self.doctor_widgets = {}
        
        self._scroll_start_y = 0
        self._scroll_start_view = 0
        
        self.setup_widgets()

    def setup_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.title_label = tk.Label(self, font=self.controller.title_font, bg='#EAF2F8')
        self.title_label.pack(pady=20)
        
        self.canvas = tk.Canvas(self, bg='#EAF2F8', highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='#EAF2F8')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y")
        
        self.doctor_widgets = {}

        for doctor in ALL_DOCTORS:
            doc_frame = tk.Frame(self.scrollable_frame, bg='white', bd=2, relief="groove")
            doc_frame.pack(fill='x', pady=5, padx=10)

            name_label = tk.Label(doc_frame, font=("Helvetica", 14, "bold"), bg='white')
            name_label.pack(pady=(5, 0))

            status_label = tk.Label(doc_frame, font=("Helvetica", 12), bg='white')
            status_label.pack()
            
            action_button = tk.Button(doc_frame, font=self.controller.button_font, fg="white", width=25)
            action_button.pack(pady=(0, 10))
            
            self.doctor_widgets[doctor["name"]] = {
                "name_label": name_label,
                "status_label": status_label,
                "action_button": action_button
            }
        
        self.bind_all_children(self.scrollable_frame)

        self.back_button = tk.Button(self, text="Back", font=self.controller.button_font, bg="#E74C3C", fg="white", command=lambda: self.controller.show_frame("WelcomeScreen"))
        self.back_button.pack(side="bottom", pady=10)
        
        self.update_language()

    def on_mousewheel(self, event):
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")

    def start_scroll(self, event):
        self._scroll_start_y = event.y
        self._scroll_start_view = self.canvas.yview()[0]

    def do_scroll(self, event):
        delta = self._scroll_start_y - event.y
        new_pos = self._scroll_start_view + (delta / self.scrollable_frame.winfo_height())
        self.canvas.yview_moveto(max(0.0, min(1.0, new_pos)))

    def bind_all_children(self, parent_widget):
        parent_widget.bind("<MouseWheel>", self.on_mousewheel)
        parent_widget.bind("<Button-4>", self.on_mousewheel)
        parent_widget.bind("<Button-5>", self.on_mousewheel)
        parent_widget.bind("<ButtonPress-1>", self.start_scroll)
        parent_widget.bind("<B1-Motion>", self.do_scroll)
        for child in parent_widget.winfo_children():
            self.bind_all_children(child)

    def notify_doctor(self, doctor_name):
        lang = self.controller.lang_manager
        messagebox.showinfo(lang.get("doctor_notified_title"), lang.get("doctor_notified_message"))
        self.controller.show_frame("WelcomeScreen")

    def update_language(self):
        lang = self.controller.lang_manager
        self.title_label.config(text=lang.get("existing_appointment_title"))
        self.back_button.config(text=lang.get("back"))
        
        # --- FIX ---
        is_hindi = lang.current_lang == "hi"

        for doctor in ALL_DOCTORS:
            widgets = self.doctor_widgets.get(doctor["name"])
            if not widgets: continue

            doctor_name_to_display = doctor.get("name_hi") if is_hindi else doctor.get("name")
            widgets["name_label"].config(text=doctor_name_to_display)

            if doctor["availability"] == "Available":
                widgets["status_label"].config(text=lang.get("available"), fg='green')
                widgets["action_button"].config(
                    text=lang.get("notify_doctor"), bg='#2ECC71', state="normal",
                    command=lambda name=doctor_name_to_display: self.notify_doctor(name)
                )
            else:
                widgets["status_label"].config(text=lang.get("unavailable"), fg='red')
                widgets["action_button"].config(text=lang.get("please_wait"), bg='grey', state="disabled")