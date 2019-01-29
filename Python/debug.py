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
Window.x, Window.y = i.pixel_search(ncon.TOP_LEFT_COLOR, 0, 0, 400, 600)

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