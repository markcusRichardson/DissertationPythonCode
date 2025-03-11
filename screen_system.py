from gpiozero import RotaryEncoder, Button
import tkinter as tk
from tkinter import ttk


# Rotary encoder 
menu = ["Brightness"]
current_option = 0
rotary = RotaryEncoder(17, 18, max_steps=10)
button = Button(27)



# Screen setup
root = tk.Tk()
root.title("E-Bike dashbaoridng")
root.geometry("1920x1080")
root.configure(bg="black")
menu_label = tk.Label(root, text=menu[current_option], font=("Helvetica", 48), fg="white", bg="black")
menu_label.pack(pady=200)



# Rotary encoder menu scolling UI
def scroll_menu ():
	global current_option
	current_option = rotary.steps % len(menu)
	print(f"selected: {menu[current_option]}")
def select_option():
	print(f"Clicked: {menu[current_option]}")
	if menu[current_option] == "exit":
		print("Exiting program...")
		exit()
rotary.when_rotated = scroll_menu
button.when_pressed = select_option

# ========
# MENU SYSTEM VARIABLES
# ========
menu_struc = {
	"Main Menu":["Security, Modes, Brightness"], 
	"Security":["Lock", "Unlock"], 
	"Modes":["Mode 1", "Mode 2", "Mode 3", "Mode 4"],
	"Brightness":["Front Lights", "Rear Lights", "Logo Lights", "Middle Lights"]
}

Brightness_setting = {
	"Front lights":50,
	"Rear lights": 50,
	"logo lights": 50,
	"Middle lights": 50
}

current_menu = "Main Menu"
current_option_index = 0
submenu_init = False  


# Labels for UI
menu_label = tk.Label(root, text="", font=("Helvetica", 24), fg="white", bg="black")
menu_label.pack(pady=20)
info_label = tk.Label(root, text="", font=("Helvetica", 18), fg="white", bg="black")
info_label.pack(pady=10)

def menu_Update_display():
	global current_menu, current_option_index
	menu_options = menu_struc[current_menu]

	displayed_menu = "/n".join([f">{option}"]) 
	if i == current_option_index else option
	for i, option in enumertae(menu_options)

def scroll_menu():
    global current_option_index, submenu_init, current_menu
    menu_options = menu_struc[current_menu]
    current_option_index = (current_option_index + 1) % len(menu_options)  # Wrap around
    menu_Update_display()

def select_current_option():
	global current_menu, submenu_init, current_option_index

	selected_option = menu_structure[current_menu][current_option_index]

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

def adjust_brightness(section):

    global brightness_levels, current_menu, current_option_index

    print(f"Adjusting {section} brightness... Turn encoder to change level.")

    def brightness_adjust():
        global brightness_levels
        while True:
            brightness_levels[section] = min(100, max(1, brightness_levels[section] + 1))
            print(f"{section} Brightness: {brightness_levels[section]}%")
            time.sleep(0.2)  # Small delay to prevent fast scrolling

    rotary.when_rotated = brightness_adjust
    button.when_pressed = lambda: exit_brightness(section)

def exit_brightness(section):
    global current_menu
    print(f"{section} brightness set to {brightness_levels[section]}%")
    current_menu = "Main Menu"
    update_menu_display()

rotary.when_rotated = scroll_menu
button.when_pressed = select_option


# Rotary encoder menu scolling UI
def scroll_menu ():
	global current_option
	current_option = rotary.steps % len(menu)
	print(f"selected: {menu[current_option]}")
def select_option():
	print(f"Clicked: {menu[current_option]}")
	if menu[current_option] == "exit":
		print("Exiting program...")
		exit()
		

threadScreen = threading.Thread(target=ScreenUpdates, daemon=True)

while (True){
	
rotary.when_rotated = scroll_menu
button.when_pressed = select_option
}

