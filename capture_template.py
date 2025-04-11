#!/usr/bin/env python3
"""
Template Capture Utility for Ubuntu AI RPA Agent
This script helps you capture UI element templates for the RPA agent.
"""

import os
import sys
import time
import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import ImageGrab, Image
import pyautogui

# Create templates directory if it doesn't exist
TEMPLATE_DIR = "templates"
os.makedirs(TEMPLATE_DIR, exist_ok=True)

class TemplateCapture:
    def __init__(self, root):
        self.root = root
        self.root.title("Template Capture Tool")
        self.root.geometry("500x300")
        self.root.resizable(False, False)
        
        # Set up the UI
        self.setup_ui()
        
        # Track selection
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.selecting = False
        
    def setup_ui(self):
        # Instructions
        title_label = tk.Label(self.root, text="UI Element Template Capture Tool", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        instructions = (
            "1. Click 'Start Capture'\n"
            "2. Position your mouse at the top-left of the UI element\n"
            "3. Press and hold left mouse button\n"
            "4. Drag to bottom-right of the element\n"
            "5. Release to capture\n"
            "6. Enter a descriptive name for the template"
        )
        
        instr_label = tk.Label(self.root, text=instructions, justify="left", padx=20)
        instr_label.pack(pady=10)
        
        # Buttons
        self.capture_button = tk.Button(self.root, text="Start Capture", command=self.start_capture, bg="#4CAF50", fg="white", height=2, width=15)
        self.capture_button.pack(pady=10)
        
        self.cancel_button = tk.Button(self.root, text="Exit", command=self.root.destroy, bg="#f44336", fg="white", height=2, width=15)
        self.cancel_button.pack(pady=5)
        
        # Status
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_label = tk.Label(self.root, textvariable=self.status_var, font=("Arial", 10, "italic"))
        status_label.pack(pady=10)
    
    def start_capture(self):
        """Initialize the screen capture process"""
        self.status_var.set("Prepare to capture (3s)...")
        self.root.update()
        self.root.withdraw()  # Hide the window
        time.sleep(3)  # Give user time to position
        
        # Create transparent overlay window
        self.overlay = tk.Toplevel(self.root)
        self.overlay.attributes("-fullscreen", True)
        self.overlay.attributes("-alpha", 0.3)
        self.overlay.attributes("-topmost", True)
        self.overlay.configure(bg="blue")
        
        # Bind mouse events
        self.overlay.bind("<ButtonPress-1>", self.on_mouse_down)
        self.overlay.bind("<B1-Motion>", self.on_mouse_drag)
        self.overlay.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.overlay.bind("<Escape>", lambda e: self.cancel_capture())
        
        # Create canvas for drawing selection rectangle
        self.canvas = tk.Canvas(self.overlay, bg="", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
    def on_mouse_down(self, event):
        """Handle mouse button press"""
        self.start_x = event.x
        self.start_y = event.y
        self.selecting = True
        self.selection_rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y, 
            outline="red", width=2
        )
        
    def on_mouse_drag(self, event):
        """Handle mouse movement while button pressed"""
        if self.selecting:
            self.end_x = event.x
            self.end_y = event.y
            self.canvas.coords(
                self.selection_rect,
                self.start_x, self.start_y, self.end_x, self.end_y
            )
            
    def on_mouse_up(self, event):
        """Handle mouse button release"""
        if not self.selecting:
            return
            
        self.end_x = event.x
        self.end_y = event.y
        self.selecting = False
        
        # Make sure coordinates are in the right order
        left = min(self.start_x, self.end_x)
        top = min(self.start_y, self.end_y)
        right = max(self.start_x, self.end_x)
        bottom = max(self.start_y, self.end_y)
        
        # Close overlay
        self.overlay.destroy()
        
        # Take the screenshot
        self.capture_area(left, top, right, bottom)
        
    def capture_area(self, left, top, right, bottom):
        """Capture the selected screen area"""
        try:
            # Take screenshot
            img = pyautogui.screenshot(region=(left, top, right-left, bottom-top))
            
            # Show the window again
            self.root.deiconify()
            
            # Ask for a name
            template_name = simpledialog.askstring(
                "Save Template", 
                "Enter a descriptive name for this UI element:",
                parent=self.root
            )
            
            if template_name:
                # Save the image
                template_path = os.path.join(TEMPLATE_DIR, f"{template_name}.png")
                img.save(template_path)
                self.status_var.set(f"Saved: {template_path}")
                messagebox.showinfo(
                    "Template Saved", 
                    f"Template saved as {template_path}\nSize: {right-left}x{bottom-top} pixels"
                )
            else:
                self.status_var.set("Capture cancelled")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to capture: {str(e)}")
    
    def cancel_capture(self):
        """Cancel the current capture operation"""
        if hasattr(self, 'overlay') and self.overlay.winfo_exists():
            self.overlay.destroy()
        self.root.deiconify()
        self.status_var.set("Capture cancelled")

if __name__ == "__main__":
    root = tk.Tk()
    app = TemplateCapture(root)
    root.mainloop()
