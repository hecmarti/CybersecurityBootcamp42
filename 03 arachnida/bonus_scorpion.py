
import imageio
import imageio.v2 as imageio
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
import os
import re
import sys
import exifread
from PIL.PngImagePlugin import PngImageFile, PngInfo

def get_images(img):

	#Abrir archivo y sacar exif
	pic = Image.open(img)
	image = imageio.imread(img)
	#gif_image = img.load()
	name = pic.filename
	exifdata = pic.getexif()

	# Creation date
	c_time = os.path.getctime(img)
	dt_c = datetime.fromtimestamp(c_time)

	# Modification date
	m_time = os.path.getmtime(img)
	dt_m = datetime.fromtimestamp(m_time)

	# Calculations
	megapixels = (pic.size[0]*pic.size[1]/1000000) # Megapixels
	d = re.sub(r'[a-z]', '', str(image.dtype)) # Dtype
	t = len(Image.Image.getbands(pic)) # Number of channels

	info_dict = {
		"Filename": pic.filename,
		"Image Height": str(pic.height),
		"Image Width": str(pic.width),
		"Image Format": pic.format,
		"Image Mode": pic.mode,
		"Creation date": str(dt_m),
		"Modification date": str(dt_c),
		"Data Type": str(image.dtype),
		"Bit Depth (per Channel)": d,
		"Bit Depth (per Pixel)": str(int(d)*int(t)),
		"Number of Channels": str(t),
		"Mode":pic.mode,
		"Megapixels": str(megapixels)
	}

	info_gif = {
		"Image is Animated": str(getattr(pic, "is_animated", False)),
		"Frames in Image": str(getattr(pic, "n_frames", 1))
	}

	print(" " + "_"*72)
	for label,value in info_dict.items():
		print(f"|{label:40}: {value:30}|")
	if pic.format == "GIF":
		for label,value in info_gif.items():
			print(f"|{label:40}: {value:30}|")
	print("|"+"·"*72+"|")
	
	if pic.format == "JPG" or pic.format == "JPEG":
		exif_tags = open(img, 'rb')
		tags = exifread.process_file(exif_tags)

		if tags == {}:
				print(f"| No available data in the {pic.format} file {name:36}|")
		else:
			for j in tags:
				aux = str(tags[j])
				if j != "JPEGThumbnail":
					print(f"|{j:40}: {aux:30}|")
	else:
		print(f"| No available data in the {pic.format} file {name:37}|")
	print(" " + "_"*72)
	
	
if __name__ == '__main__':
	arguments = len(sys.argv[1:])
	if arguments < 1:
		print("Please specify an Image file")
		exit()
	ext = [".png", ".jpg", ".jpeg", ".gif", ".bmp"]
	for i in range(1, arguments + 1):
		name, extension = os.path.splitext(sys.argv[i])
		if extension not in ext:
			print("File format not supported")
		else:
			get_images(sys.argv[i])
	#print(" " + "_"*67)
	print("Finished!")
