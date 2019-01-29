from PIL import Image
import os
from PIL import ImageFilter



def rgb_to_hex(tup):
	"""Convert RGB value to HEX."""
	return '%02x%02x%02x'.upper() % (tup[0], tup[1], tup[2])

def pixel_search(bmp, color, x_start, y_start, x_end, y_end):
	"""Find the first pixel with the supplied color within area.
	Function searches per row, left to right. Returns the coordinates of
	first match or None, if nothing is found.
	Color must be supplied in hex.
	"""
	width, height = bmp.size
	for y in range(y_start, y_end):
		for x in range(x_start, x_end):
			if y > height or x > width:
				continue
			t = bmp.getpixel((x, y))
			if (rgb_to_hex(t) == color):
				return x, y
	return None



mypath = "Pic\\"
onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]

bmp = Image.open(os.path.join(mypath, onlyfiles[0]))
startX, startY = pixel_search(bmp, "000408", 10,10,400,400)
startX += 1
startY += 1



HasFolder = []
subFolder = ""
for i in onlyfiles:
	splitVal = i.split('_')
	subFolder = os.path.join(mypath, splitVal[0])
	
	if splitVal[0] not in HasFolder:
		if not os.path.exists(subFolder):
			os.makedirs(subFolder)
		HasFolder.append(splitVal[0])


	bmp = Image.open(os.path.join(mypath, i))
	bmp = bmp.crop((startX, startY, 958 + startX, 598 + startY))
	
	*_, right, lower = bmp.getbbox()
	bmp = bmp.resize((right*3, lower*3), Image.BICUBIC)  # Resize image
	bmp = bmp.filter(ImageFilter.SHARPEN)  # Sharpen image for better OCR
	
	bmp.save(os.path.join(subFolder, splitVal[1]))
	os.remove(os.path.join(mypath, i))