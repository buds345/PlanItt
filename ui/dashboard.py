import customtkinter as ctk
import os
from PIL import Image, ImageTk

class DashboardPage(ctk.CTkFrame):
    def __init__(self, master, user_data, navigate_callback):
        super().__init__(master)
        self.master = master
        self.user_data = user_data
        self.username = user_data["username"]
        self.navigate_callback = navigate_callback  # Dictionary with navigation callbacks

        self.pack(fill="both", expand=True)
        self.build_ui()

    def build_ui(self):
        self.configure(fg_color="#FFB6C1")  # Set background of entire dashboard

        # Configure rows and columns for main content centering
        self.grid_rowconfigure(0, weight=0)  # Header row
        self.grid_rowconfigure(1, weight=1)  # Content row (will be centered)
        self.grid_columnconfigure(0, weight=1)  # Center column

        # Welcome Label
        welcome = ctk.CTkLabel(
            self, 
            text=f"Welcome, {self.username}", 
            font=("Georgia", 30, "bold"), 
            text_color="black"
        )
        # Configure rows for vertical spacing
        self.grid_rowconfigure(0, weight=1)  # Spacer row (pushes content down)
        welcome.grid(row=0, column=0, pady=(40, 30))
        self.grid_rowconfigure(2, weight=1)  # Content/buttons (optional center alignment)

        

        # Create a central frame to hold all the buttons
        center_frame = ctk.CTkFrame(self, fg_color="transparent")
        center_frame.grid(row=1, column=0)
        
        # Configure the center frame's grid
        center_frame.grid_columnconfigure(0, weight=1)
        center_frame.grid_columnconfigure(1, weight=1)

        # Define buttons
        buttons = [
            {"text": "Profile", "image": "ui/profile.png", "command": self.navigate_callback["profile"]},
            {"text": "Create Event", "image": "ui/add_event.png", "command": self.navigate_callback["create_event"]},
            {"text": "Events", "image": "ui/events.png", "command": self.navigate_callback["events"]},
            {"text": "Schedule", "image": "ui/schedule.png", "command": self.navigate_callback["schedule"]},
        ]

        # Position buttons in a 2x2 grid with reduced spacing
        positions = [
            (0, 0),  # Profile: top-left
            (0, 1),  # Create Event: top-right
            (1, 0),  # Events: bottom-left
            (1, 1),  # Schedule: bottom-right
        ]

        # Spacing between buttons (reduce these values to bring buttons closer)
        button_padx = 15  # Horizontal spacing between buttons
        button_pady = 30  # Vertical spacing between rows

        for i, btn in enumerate(buttons):
            row, col = positions[i]
            
            # Create a frame for each button section
            btn_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
            btn_frame.grid(row=row, column=col, padx=button_padx, pady=button_pady)
            
            # Add the icon
            if os.path.exists(btn["image"]):
                img = Image.open(btn["image"]).resize((80, 80))
                icon = ImageTk.PhotoImage(img)
                img_label = ctk.CTkLabel(btn_frame, image=icon, text="")
                img_label.image = icon  # Keep a reference to prevent garbage collection
                img_label.grid(row=0, column=0)
            
            # Add the button
            ctk.CTkButton(
                btn_frame,
                text=btn["text"],
                command=btn["command"],
                width=160,
                height=40,
                font=("Segoe UI", 16),
                fg_color="#ff69b4",
                hover_color="#ff1493",
                text_color="white",
                corner_radius=10
            ).grid(row=1, column=0, pady=(1, 0))  # Minimal padding