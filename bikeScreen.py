from gpiozero import RotaryEncoder, Button
from signal import pause
import tkinter as tk
from tkinter import ttk

rotary = RotaryEncoder(17,18,max_steps=10)
button = Button(27)

menu=["Speed", "battery", "Settings", "Exit"]
current_option = 0


root = tk.Tk()
root.title("E-Bike dashbaoridng")
root.geometry("1920x1080")
root.configure(bg="black")

menu_label = tk.Label(root, text=menu[current_option], font=("Helvetica", 48), fg="white", bg="black")
menu_label.pack(pady=200)




def update_menu():
	global current_option
	current_option = rotary.steps % len(menu)
	menu_label.config(text=menu[current_option])
	

def select_menu():
	print(f"Selected: {menu[current_option]}")
	if menu[current_option] == "Exit":
		root.destroy()
rotary.when_rotated = update_menu
button.when_pressed = select_menu

print("Encoder ready")
root.mainloop()


update_dashboard()
root.mainloop()

