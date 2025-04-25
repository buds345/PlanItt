import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from tkinter import messagebox

from auth.register import register_user
from auth.login import login_user
from events_gui import EventDashboard


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")  # Optional custom theme later

class AuthApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PlanIt - Event App")
        self.geometry("400x500")
        self.resizable(True, True)

        self.mode = "login"
        self.build_login_ui()

    def clear_ui(self):
        for widget in self.winfo_children():
            widget.destroy()

    def build_login_ui(self):
        self.clear_ui()
        ctk.CTkLabel(self, text="Sign In", font=("Segoe UI", 22)).pack(pady=20)

        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email")
        self.email_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        ctk.CTkButton(self, text="Login", command=self.handle_login, fg_color="#ff007f").pack(pady=20)

        ctk.CTkButton(self, text="No account? Register", command=self.build_register_ui, fg_color="transparent", border_color="#ff007f", border_width=2, text_color="#ff007f").pack()

    def build_register_ui(self):
        self.clear_ui()
        ctk.CTkLabel(self, text="Register", font=("Segoe UI", 22)).pack(pady=20)

        self.name_entry = ctk.CTkEntry(self, placeholder_text="Name")
        self.name_entry.pack(pady=10)

        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email")
        self.email_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        ctk.CTkButton(self, text="Register", command=self.handle_register, fg_color="#ff007f").pack(pady=20)

        ctk.CTkButton(self, text="Already registered? Sign In", command=self.build_login_ui, fg_color="transparent", border_color="#ff007f", border_width=2, text_color="#ff007f").pack()

    def handle_login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        user = login_user(email, password)
        if user:
            messagebox.showinfo("Success", "Login successful!")
            self.show_event_dashboard(user)
        else:
            messagebox.showerror("Error", "Invalid credentials.")
    
    def show_event_dashboard(self, user_data):
        self.clear_ui()
        self.dashboard = EventDashboard(self, user_data)    

    def handle_register(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        if register_user(name, email, password):
            messagebox.showinfo("Success", "Registration successful!")
            self.build_login_ui()
        else:
            messagebox.showerror("Error", "Registration failed.")

if __name__ == "__main__":
    app = AuthApp()
    app.mainloop()
