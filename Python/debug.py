import win32api
import win32gui
import time

from classes.window import Window
from classes.inputs import Inputs

import ngucon as ncon


w = "derp"
try:
	w = Window(debug=True)
except:
	print("Could not find debug game window")
	a = input("Do you want me to use main window? (Y/N)")
	if a.lower() == "y":
		w = Window()
	else:
		print("closing script")
		quit()	
i = Inputs()
Window.x, Window.y = i.pixel_search(ncon.TOP_LEFT_COLOR, 10, 10, 400, 600)


def get_pixel_color(x, y):
	def rgb_to_hex(tup):
		"""Convert RGB value to HEX."""
		return '%02x%02x%02x'.upper() % (tup[0], tup[1], tup[2])

	"""Get the color of selected pixel in HEX."""
	dc = win32gui.GetWindowDC(Window.id)
	rgba = win32gui.GetPixel(dc, x + 8 + Window.x, y + 8 + Window.y)
	win32gui.ReleaseDC(Window.id, dc)
	r = rgba & 0xff
	g = rgba >> 8 & 0xff
	b = rgba >> 16 & 0xff
	return rgb_to_hex((r, g, b))


	def pixel_search(self, color, x_start, y_start, x_end, y_end):
		"""Find the first pixel with the supplied color within area.

		Function searches per row, left to right. Returns the coordinates of
		first match or None, if nothing is found.

		Color must be supplied in hex.
		"""
		bmp = self.get_bitmap()
		width, height = bmp.size
		for y in range(y_start, y_end):
			for x in range(x_start, x_end):
				if y > height or x > width:
					continue
				t = bmp.getpixel((x, y))
				if (self.rgb_to_hex(t) == color):
					return x - 8, y - 8

		return None
	
'''
for y in range(313 - 1, 329 + 1):
	for x in range(702 - 1, 751 + 1):
		pixel = get_pixel_color(x, y)
		if pixel == "000000":
			win32api.SetCursorPos((Window.x + x, Window.y + y))
			print(f"X={x} Y={y} Pixel={pixel}")
			input("FOUND IT")
'''


'''
print(w.x, w.y)
win32api.SetCursorPos((w.x + 630, w.y + 290))
currentMousePos = win32api.GetCursorPos()
print("No Mod -     X=" + str(currentMousePos[0]) + " Y=" + str(currentMousePos[1]))
print("Game Only  - X=" + str(currentMousePos[0] - w.x) + " Y=" + str(currentMousePos[1] - w.y))
'''

while True:
	tempVal = win32api.GetCursorPos()
	#print("X=" + str(tempVal[0]) + " Y=" + str(tempVal[1]))
	print("X=" + str(tempVal[0] - w.x) + " Y=" + str(tempVal[1] - w.y))
	#print("X=" + str(tempVal[0] - herpLeDerp[0]) + " Y=" + str(tempVal[1] - herpLeDerp[1]))
	time.sleep(0.05)