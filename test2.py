from PIL import Image
import operator
from collections import defaultdict
import re

input_path = 'brick-house.png'
output_path = 'outputtest2.png'

# Defines number of pixels squared, that ultimately decide HOW pixelated the image is 
legosize = 3 



img = Image.open(input_path)
img = img.quantize(palette=palette_img) #use only the palette 
img = img.convert('RGB')

input_width= img.size[1]
input_height= img.size[0]

# At this part use the % operator to see the excess pixels that dont fit when using a pixel array. What to do? Scale? 

for x_height in range(0,(img.size[0] // legosize),legosize): 
	for x_width in range (0,(img.size[1] // legosize),legosize): 
		print ("Height: ",x_height)
		print ("Width: ",x_width)
		box = (x_height, x_width,x_height+legosize, x_width+legosize)
		region = img.crop(box)
		region = region.transpose(Image.ROTATE_180)
		img.paste(region, box)
