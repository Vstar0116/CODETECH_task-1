import re
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Progressbar, Style
from PIL import Image, ImageTk
import random
import string

# Constants for styling
MIN_LENGTH = 8
MAX_SCORE = 5
PRIMARY_COLOR = "#4CAF50"
SECONDARY_COLOR = "#2196F3"
FONT_TITLE = ("Roboto", 20, "bold")
FONT_LABEL = ("Roboto", 12, "bold")

# Helper functions for password validation
def has_digit(password):
    return bool(re.search(r"\d", password))

def has_uppercase(password):
    return bool(re.search(r"[A-Z]", password))

def has_lowercase(password):
    return bool(re.search(r"[a-z]", password))

def has_special_char(password):
    return bool(re.search(r"\W", password))

# Function to check password strength
def check_password_strength(password, min_length=MIN_LENGTH):
    length_error = len(password) < min_length
    digit_error = not has_digit(password)
    uppercase_error = not has_uppercase(password)
    lowercase_error = not has_lowercase(password)
    special_char_error = not has_special_char(password)

    errors = []
    strength_score = 0

    if not length_error:
        strength_score += 1
    if not digit_error:
        strength_score += 1
    if not uppercase_error:
        strength_score += 1
    if not lowercase_error:
        strength_score += 1
    if not special_char_error:
        strength_score += 1

    if length_error:
        errors.append(f"Password should be at least {min_length} characters long.")
    if digit_error:
        errors.append("Password should contain at least one digit.")
    if uppercase_error:
        errors.append("Password should contain at least one uppercase letter.")
    if lowercase_error:
        errors.append("Password should contain at least one lowercase letter.")
    if special_char_error:
        errors.append("Password should contain at least one special character.")

    return {
        "is_strong": strength_score == MAX_SCORE,
        "errors": errors,
        "strength_score": strength_score
    }

# Function to generate password suggestions
def suggest_password():
    suggestions = []
    for _ in range(3):  # Generate 3 suggestions
        password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=12))
        suggestions.append(password)
    suggestions_text.set("\n".join(suggestions))

# Function to check password and update feedback
def check_password():
    password = password_entry.get()
    result = check_password_strength(password)

    strength_score = result["strength_score"]
    strength_bar["value"] = strength_score * 20

    # Update the progress bar color based on strength score
    if strength_score == MAX_SCORE:
        feedback_label.config(text="Very Strong", fg=PRIMARY_COLOR)
        strength_bar_style.configure("TProgressbar", troughcolor='#e0e0e0', background=PRIMARY_COLOR)  # Green
    elif strength_score == 4:
        feedback_label.config(text="Strong", fg=SECONDARY_COLOR)
        strength_bar_style.configure("TProgressbar", troughcolor='#e0e0e0', background=SECONDARY_COLOR)  # Blue
    elif strength_score == 3:
        feedback_label.config(text="Medium", fg="#FF9800")
        strength_bar_style.configure("TProgressbar", troughcolor='#e0e0e0', background='#FF9800')  # Orange
    elif strength_score == 2:
        feedback_label.config(text="Weak", fg="#F44336")
        strength_bar_style.configure("TProgressbar", troughcolor='#e0e0e0', background='#F44336')  # Red
    else:
        feedback_label.config(text="Very Weak", fg="#D32F2F")
        strength_bar_style.configure("TProgressbar", troughcolor='#e0e0e0', background='#D32F2F')  # Darker Red

    if result["is_strong"]:
        errors_text.set("")
    else:
        errors_text.set("\n".join(result["errors"]))

# Function to toggle password visibility
def toggle_password_visibility():
    if password_entry.cget("show") == "*":
        password_entry.config(show="")
        toggle_button.config(image=hide_icon)
    else:
        password_entry.config(show="*")
        toggle_button.config(image=show_icon)

# Create the main application window
root = tk.Tk()
root.title("Professional Password Strength Checker")
root.geometry("500x650")
root.configure(bg="#f5f5f5")

# Set window icon (top left corner)
try:
    app_icon = ImageTk.PhotoImage(Image.open("D:\projects\codetech intenship\Application_icon.png"))
    root.iconphoto(False, app_icon)
except FileNotFoundError:
    messagebox.showerror("Error", "Application icon not found")

# Load icons for show/hide password
try:
    show_icon = ImageTk.PhotoImage(Image.open("D:/projects/codetech internship/images/show icon.png").resize((20, 20)))
    hide_icon = ImageTk.PhotoImage(Image.open("D:/projects/codetech internship/images/hide icon.jpg").resize((20, 20)))
except FileNotFoundError:
    show_icon = None
    hide_icon = None
    messagebox.showerror("Error", "Required icons not found")

# Create a style for the progress bar
strength_bar_style = Style(root)
strength_bar_style.configure("TProgressbar", thickness=20)

# Add title label with a sleek font
title_label = tk.Label(root, text="Password Strength Checker", font=FONT_TITLE, bg="#f5f5f5", fg="#333")
title_label.pack(pady=20)

# Frame for password entry and icon
password_frame = tk.Frame(root, bg="#f5f5f5")
password_frame.pack(pady=10)

# Password input
password_entry = tk.Entry(password_frame, width=30, show="*", font=("Helvetica", 12))
password_entry.pack(side="left", padx=10)

# Add a toggle button to show/hide the password
if show_icon:
    toggle_button = tk.Button(password_frame, image=show_icon, command=toggle_password_visibility, bg="#e0e0e0", borderwidth=0)
    toggle_button.pack(side="left")
else:
    toggle_button = tk.Button(password_frame, text="Show", command=toggle_password_visibility, bg="#e0e0e0", borderwidth=0)
    toggle_button.pack(side="left")

# Progress bar for password strength
strength_bar = Progressbar(root, orient="horizontal", mode="determinate", maximum=100, length=400, style="TProgressbar")
strength_bar.pack(pady=20)

# Button to check password strength
check_button = tk.Button(root, text="Check Password Strength", command=check_password, font=FONT_LABEL, bg=PRIMARY_COLOR, fg="white")
check_button.pack(pady=10)

# Feedback label for password strength
feedback_label = tk.Label(root, text="", font=("Roboto", 12, "bold"), bg="#f5f5f5")
feedback_label.pack(pady=5)

# Label to display errors if the password is weak
errors_text = tk.StringVar()
errors_label = tk.Label(root, textvariable=errors_text, fg="red", bg="#f5f5f5", justify="left", wraplength=400)
errors_label.pack(pady=5)

# Password suggestions
suggestions_label = tk.Label(root, text="Password Suggestions:", font=FONT_LABEL, bg="#f5f5f5")
suggestions_label.pack(pady=5)

suggestions_text = tk.StringVar()
suggestions_display = tk.Label(root, textvariable=suggestions_text, font=("Helvetica", 10), bg="#f5f5f5", fg="#333", justify="left", wraplength=400)
suggestions_display.pack(pady=5)

# Button to generate password suggestions
suggest_button = tk.Button(root, text="Suggest Password", command=suggest_password, font=FONT_LABEL, bg=SECONDARY_COLOR, fg="white")
suggest_button.pack(pady=10)

# Start the GUI event loop
root.mainloop()
