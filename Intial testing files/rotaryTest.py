from gpiozero import RotaryEncoder, Button
from signal import pause

rotary = RotaryEncoder(17, 18, max_steps=10)
button = Button(27)

menu = ["Speed", "battery", "Settings", "Exit"]
current_option = 0

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

print("READY")
pause()

