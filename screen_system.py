# ===================================================
# Smart Bike Display System – Dashboard UI for Pi
# ---------------------------------------------------
# This script creates a fullscreen graphical interface on a 3.5" Raspberry Pi display,
# allowing the rider to interact with the smart bike using a rotary encoder and button.
# It displays key information (speed, GPS, brightness) and allows navigation
# of a menu to change lock state, brightness levels, and operational modes.
# ===================================================

from gpiozero import RotaryEncoder, Button  # Hardware input controls
import tkinter as tk                        # GUI toolkit
import threading                            # Threading for background tasks
import configV                              # Shared configuration module
import time                                 # Timing functions

# ----------------------------
# Rotary Encoder Configuration
# ----------------------------
current_option = 0  # Currently highlighted option in the menu

# Initialize rotary encoder only if not already defined (avoid re-initialization)
if 'rotary' not in globals():
    rotary = RotaryEncoder(17, 18, max_steps=10)  # GPIO pins for encoder
    button = Button(27)                           # GPIO pin for button

# ----------------------------
# Menu Structure
# ----------------------------
# Defines the nested menu system used on the display
menu_struc = {
    "Main Menu": ["Security", "Modes", "Brightness"],
    "Security": ["Lock", "Unlock"],
    "Modes": ["Mode 1", "Mode 2", "Mode 3", "Mode 4"],
    "Brightness": ["Front Lights", "Rear Lights", "Logo Lights", "Middle Lights"]
}

# Track menu navigation
current_menu = "Main Menu"
current_option_index = 0
submenu_init = False

# ----------------------------
# GUI Initialization
# ----------------------------
root = tk.Tk()
root.overrideredirect(True)         # Remove window decorations
root.attributes("-fullscreen", True)
root.configure(bg="black")          # Black background for night visibility

# ----------------------------
# Setup GUI Elements
# ----------------------------
def dashboard_setup():
    """
    Initializes all UI labels and layout for the dashboard display.
    Includes title, speed, time, GPS, brightness, and menu areas.
    """
    global root, title_label, time_label, menu_label, speed_label, coordinates_label, brightness_label

    root.title("Ebike Dashboard")
    root.geometry("1920x1080")
    root.configure(bg="black")

    # Title bar and system time
    title_label = tk.Label(root, text="E-Bike Dashboard", font=("Helvetica", 36), fg="white", bg="black")
    title_label.grid(row=0, column=1, columnspan=2, pady=10, sticky="n")

    time_label = tk.Label(root, text="Time: 00:00", font=("Helvetica", 24), fg="white", bg="black")
    time_label.grid(row=0, column=2, padx=20, sticky="ne")

    # Menu area (left)
    menu_label = tk.Label(root, text="Menu", font=("Helvetica", 24), fg="white", bg="black")
    menu_label.grid(row=1, column=0, rowspan=4, padx=20, sticky="w")

    # Speed display (center)
    speed_label = tk.Label(root, text="Speed: 0 km/h", font=("Helvetica", 50), fg="white", bg="black")
    speed_label.grid(row=2, column=1, pady=20, sticky="nsew")

    # GPS coordinates (top-right)
    coordinates_label = tk.Label(root, text="GPS: 0.000, 0.000", font=("Helvetica", 24), fg="white", bg="black")
    coordinates_label.grid(row=1, column=2, padx=20, sticky="ne")

    # Brightness levels (bottom-right)
    brightness_label = tk.Label(root, text="Brightness\nFront: 0\nMiddle: 0\nRear: 0",
                                font=("Helvetica", 20), fg="white", bg="black", justify="left")
    brightness_label.grid(row=3, column=2, padx=20, sticky="se")

# ----------------------------
# Real-time Display Updates
# ----------------------------
def update_display():
    """
    Continuously updates speed, GPS, time, and brightness information
    using shared config values updated via serial communication.
    """
    speed_label.config(text=f"Speed: {configV.speed} km/h")
    coordinates_label.config(text=f"GPS: {configV.latitude}, {configV.longitude}")
    time_label.config(text=f"Time: {configV.time}")
    brightness_label.config(text=f"Brightness\nFront: {configV.brightnessFront}\nMiddle: {configV.brightnessMiddle}\nRear: {configV.brightnessRear}")
    root.after(100, update_display)  # Schedule next update (every 100ms)

# ----------------------------
# Menu Navigation Display
# ----------------------------
def menu_Update_display():
    """
    Updates the menu section based on the current menu and selected option.
    Highlights the current selection using ">" symbol.
    """
    global current_menu, current_option_index
    menu_options = menu_struc[current_menu]

    displayed_menu = "\n".join([
        f"> {option}" if i == current_option_index else option
        for i, option in enumerate(menu_options)
    ])

    menu_label.config(text=displayed_menu)

# ----------------------------
# Menu Scrolling Logic
# ----------------------------
def scroll_menu():
    """
    Scrolls through menu items when rotary encoder is rotated.
    """
    global current_option_index, current_menu
    menu_options = menu_struc[current_menu]
    current_option_index = (current_option_index + 1) % len(menu_options)  # Wrap around
    menu_Update_display()

# ----------------------------
# Menu Selection Logic
# ----------------------------
def select_current_option():
    """
    Handles the selection of the currently highlighted option via button press.
    Navigates into submenus or returns to main menu as appropriate.
    """
    global current_menu, current_option_index

    selected_option = menu_struc[current_menu][current_option_index]

    if current_menu == "Main Menu":
        current_menu = selected_option
        current_option_index = 0
        menu_Update_display()
    elif current_menu in ["Security", "Brightness", "Modes"]:
        current_menu = "Main Menu"
        menu_Update_display()

# ----------------------------
# Brightness Adjustment Logic
# ----------------------------
def adjust_brightness(section):
    """
    Increments the brightness level for the given section (front, rear, logo, middle).
    Triggered when rotary is turned in a brightness submenu.
    """
    global current_menu, current_option_index

    print(f"Adjusting {section} brightness... Turn encoder to change level.")

    if section == "Front Lights":
        configV.brightnessFront = min(100, max(0, configV.brightnessFront + 1))
        brightness_label.config(text=f"Front Brightness: {configV.brightnessFront}%")

    elif section == "Rear Lights":
        configV.brightnessRear = min(100, max(0, configV.brightnessRear + 1))
        brightness_label.config(text=f"Rear Brightness: {configV.brightnessRear}%")

    elif section == "Logo Lights":
        configV.brightnessLogo = min(100, max(0, configV.brightnessLogo + 1))
        brightness_label.config(text=f"Logo Brightness: {configV.brightnessLogo}%")

    elif section == "Middle Lights":
        configV.brightnessMiddle = min(100, max(0, configV.brightnessMiddle + 1))
        brightness_label.config(text=f"Middle Brightness: {configV.brightnessMiddle}%")

# ----------------------------
# Exit Brightness Mode
# ----------------------------
def exit_brightness(section):
    """
    Finalizes brightness value and returns to the main menu.
    Called when the user presses the button in a brightness submenu.
    """
    global current_menu

    # Optionally clamp values here again (already done in adjust)
    configV.current_menu = "Main Menu"
    menu_Update_display()

# ----------------------------
# Main Function to Start UI
# ----------------------------
def start_screen():
    """
    Launches the GUI, attaches rotary encoder events, and enters the main event loop.
    """
    dashboard_setup()
    update_display()

    # Connect rotary and button events to their handlers
    rotary.when_rotated = scroll_menu
    button.when_pressed = select_current_option

    # If you want brightness adjustment to be active during those menus, replace above with:
    # rotary.when_rotated = lambda: adjust_brightness(current_option)
    # button.when_pressed = lambda: exit_brightness(current_option)

    root.mainloop()
