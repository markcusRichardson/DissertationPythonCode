import threading
import time
import Serial_handling
import mqtt_handler
import screen_system
import struct
import configV
import sys
from gpiozero import RotaryEncoder, Button
import tkinter as tk

current_option = 0
rotary = RotaryEncoder(17, 18, max_steps=10)
button = Button(27)

# MENU setup variables
menu_struc = {
	"Main Menu":["Security, Modes, Brightness"], 
	"Security":["Lock", "Unlock"], 
	"Modes":["Mode 1", "Mode 2", "Mode 3", "Mode 4"],
	"Brightness":["Front Lights", "Rear Lights", "Logo Lights", "Middle Lights"]
}

current_menu = "Main Menu"
current_option_index = 0
submenu_init = False  
root = tk.Tk()
setup_done = False
# SETUP the display
def dashboard_setup():
    if setup_done:
        return  # If already run, exit immediately
    global root, title_label, time_label, menu_label, speed_label, coordinates_label, brightness_label
    # Rotary encoder setup variables
    
    root.overrideredirect(True)
    root.attributes("-fullscreen", True)
    root.configure(bg="black")  
    root.title("Ebike dashboard")
    root.geometry("1920x1080")
    root.configure(bg="black")


    # Top Section (Title & Time)
    title_label = tk.Label(root, text="E-Bike Dashboard", font=("Helvetica", 36), fg="white", bg="black")
    title_label.grid(row=0, column=1, columnspan=2, pady=10, sticky="n")

    time_label = tk.Label(root, text="Time: 00:00", font=("Helvetica", 24), fg="white", bg="black")
    time_label.grid(row=0, column=2, padx=20, sticky="ne")

    # Left Section (Menu)
    menu_label = tk.Label(root, text="Menu", font=("Helvetica", 24), fg="white", bg="black")
    menu_label.grid(row=1, column=0, rowspan=4, padx=20, sticky="w")

    # Center Section (Speed)
    speed_label = tk.Label(root, text="Speed: 0 km/h", font=("Helvetica", 50), fg="white", bg="black")
    speed_label.grid(row=2, column=1, pady=20, sticky="nsew")

    # Top Right Section (Coordinates)
    coordinates_label = tk.Label(root, text="GPS: 0.000, 0.000", font=("Helvetica", 24), fg="white", bg="black")
    coordinates_label.grid(row=1, column=2, padx=20, sticky="ne")

    # Bottom Right Section (Brightness Levels)
    brightness_label = tk.Label(root, text="Brightness\nFront: 0\nMiddle: 0\nRear: 0", font=("Helvetica", 20), fg="white", bg="black", justify="left")
    brightness_label.grid(row=3, column=2, padx=20, sticky="se")

def update_display():
	speed_label.config(text=f"Speed: {configV.speed} km/h")
	coordinates_label.config(text=f"GPS: {configV.latitude}, {configV.longitude}")
	time_label.config(text=f"Time: {configV.time}")
	brightness_label.config(text=f"Brightness\nFront: {configV.brightnessFront}\nMiddle: {configV.brightnessMiddle}\nRear: {configV.brightnessRear}")
	root.after(100, update_display)  # Re-run every 1 second

def menu_Update_display():
    global current_menu, current_option_index
    menu_options = menu_struc[current_menu]

    displayed_menu = "\n".join([
    f"> {option}" if i == current_option_index else option
    for i, option in enumerate(menu_options)
	])

    menu_label.config(text=displayed_menu)


# Rotary encoder menu scolling UI
def scroll_menu():
    global current_option_index, submenu_init, current_menu
    menu_options = menu_struc[current_menu]
    current_option_index = (current_option_index + 1) % len(menu_options)  # Wrap around
    menu_Update_display()

def select_current_option():
	global current_menu, submenu_init, current_option_index, menu_struc

	selected_option = menu_struc[current_menu][current_option_index]

	if current_menu == "Main Menu":
		current_menu = selected_option
		current_option_index = 0
		menu_Update_display()
	elif current_menu == "Security":
		current_menu == "Main menu"
		menu_Update_display()
	elif current_menu == "Brightness":
		current_menu == "Brightness"
		menu_Update_display()
	elif current_menu == "Modes":
		current_menu == "Modes"
		menu_Update_display()


# Adjust brigtness
def adjust_brightness(section):

    global current_menu, current_option_index

    print(f"Adjusting {section} brightness... Turn encoder to change level.")

    def brightness_adjust(): 
        if section == "Front Lights":
            configV.brightnessFront = min(100, max(0, configV.brightnessFront + 1))
            brightness_label.config(text=f"Front Brightness: {configV.brightnessFront}%")
            print(f"Front Lights Brightness: {configV.brightnessFront}%")

        elif section == "Rear Lights":
            configV.brightnessRear = min(100, max(0, configV.brightnessRear + 1))
            brightness_label.config(text=f"Rear Brightness: {configV.brightnessRear}%")
            print(f"Rear Lights Brightness: {configV.brightnessRear}%")

        elif section == "Logo Lights":
            configV.brightnessLogo = min(100, max(0, configV.brightnessLogo + 1))
            brightness_label.config(text=f"Logo Brightness: {configV.brightnessLogo}%")
            print(f"Logo Lights Brightness: {configV.brightnessLogo}%")

        elif section == "Middle Lights":
            configV.brightnessMiddle = min(100, max(0, configV.brightnessMiddle + 1))
            brightness_label.config(text=f"Middle Brightness: {configV.brightnessMiddle}%")
            print(f"Middle Lights Brightness: {configV.brightnessMiddle}%")

def exit_brightness(section):
    global current_menu

    # Ensure the correct brightness setting is stored in configV
    if section == "Front Lights":
        configV.brightnessFront = min(100, max(0, configV.brightnessFront))
        print(f"✅ Front Lights Brightness set to {configV.brightnessFront}%")

    elif section == "Rear Lights":
        configV.brightnessRear = min(100, max(0, configV.brightnessRear))
        print(f"✅ Rear Lights Brightness set to {configV.brightnessRear}%")

    elif section == "Logo Lights":
        configV.brightnessLogo = min(100, max(0, configV.brightnessLogo))
        print(f"✅ Logo Lights Brightness set to {configV.brightnessLogo}%")

    elif section == "Middle Lights":
        configV.brightnessMiddle = min(100, max(0, configV.brightnessMiddle))
        print(f"✅ Middle Lights Brightness set to {configV.brightnessMiddle}%")

    # Switch back to the main menu
    configV.current_menu = "Main Menu"
    menu_Update_display()



# Running all of the code
def start_threads():
    serial_thread = threading.Thread(target=Serial_handling.serial_task, daemon=True)
    mqtt_thread = threading.Thread(target=mqtt_handler.mqtt_task, daemon=True)
    serial_thread.start()
    mqtt_thread.start()


start_threads()
dashboard_setup()
setup_done = True
update_display()
rotary.when_rotated = scroll_menu
button.when_pressed = select_current_option
rotary.when_rotated = lambda: adjust_brightness(current_option)
button.when_pressed = lambda: exit_brightness(current_option)
root.mainloop()