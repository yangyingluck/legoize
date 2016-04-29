from PIL import Image
import operator
from collections import defaultdict
import re
import functools

input_path = 'brick-house.png'
output_path = 'output.png'

size = (44,60)


simple_palette = [
    (45,  50,  50),  #black
    (240, 68,  64),  #red
    (211, 223, 223), #white
    (160, 161, 67),  #green
    (233, 129, 76),  #orange
]

#The true palette of all appropriate lego brick colors 
#http://isodomos.com/Color-Tree/Lego-List.html

palette = [
	(161,165,162), #Grey
	(249,233,153), #Light yellow
	(215,197,153), #Brick yellow
	(194,218,184), #Light green (Mint)
	(232,186,199), #Light reddish violet
	(203,132,66), #Light orange brown
	(204,142,104), #Nougat
	(196,40,27), #Bright red
	(196,112,160), #Med. reddish violet
	(13,105,171), #Bright blue
	(245,205,47), #Bright yellow
	(98,71,50), #Earth orange
	(27,42,52), #Black
	(109,110,108), #Dark grey
	(40,127,70), #Dark green
	(161,196,139), #Medium green
	(243,207,155), #Lig. Yellowich orange
	(75,151,74), #Bright green
	(160,95,52), #Dark orange
	(193,202,222), #Light bluish violet
	(205,84,75), #Tr. Red
	(193,223,240), #Tr. Lg blue
	(123,182,232), #Tr. Blue
	(247,241,141), #Tr. Yellow
	(180,210,227), #Light blue
	(217,133,108), #Tr. Flu. Reddish orange
	(132,182,141), #Tr. Green
	(248,241,132), #Tr. Flu. Green
	(236,232,222), #Phosph. White
	(238,196,182), #Light red
	(218,134,121), #Medium red
	(110,153,201), #Medium blue
	(199,193,183), #Light grey
	(107,50,123), #Bright violet
	(226,155,63), #Br. yellowish orange
	(218,133,64), #Bright orange
	(0,143,155), #Bright bluish green
	(104,92,67), #Earth yellow
	(67,84,147), #Bright bluish violet
	(191,183,177), #Tr. Brown
	(104,116,172), #Medium bluish violet
	(228,173,200), #Tr. Medi. reddish violet
	(199,210,60), #Med. yellowish green
	(85,165,175), #Med. bluish green
	(183,215,213), #Light bluish green
	(164,189,70), #Br. yellowish green
	(217,228,167), #Lig. yellowish green
	(231,172,88), #Med. yellowish orange
	(211,111,76), #Br. reddish orange
	(146,57,120), #Bright reddish violet
	(234,184,145), #Light orange
	(165,165,203), #Tr. Bright bluish violet
	(220,188,129), #Gold
	(174,122,89), #Dark nougat
	(156,163,168), #Silver
	(213,115,61), #Neon orange
	(216,221,86), #Neon green
	(116,134,156), #Sand blue
	(135,124,144), #Sand violet
	(224,152,100), #Medium orange
	(149,138,115), #Sand yellow
	(32,58,86), #Earth blue
	(39,70,44), #Earth green
	(207,226,247), #Tr. Flu. Blue
	(121,136,161), #Sand blue metallic
	(149,142,163), #Sand violet metallic
	(147,135,103), #Sand yellow metallic
	(87,88,87), #Dark grey metallic
	(22,29,50), #Black metallic
	(171,173,172), #Light grey metallic
	(120,144,129), #Sand green
	(149,121,118), #Sand red
	(123,46,47), #Dark red
	(255,246,123), #Tr. Flu. Yellow
	(225,164,194), #Tr. Flu. Red
	(117,108,98), #Gun metallic
	(151,105,91), #Red flip/flop
	(180,132,85), #Yellow flip/flop
	(137,135,136), #Silver flip/flop
	(215,169,75), #Curry
	(249,214,46), #Fire Yellow
	(232,171,45), #Flame yellowish orange
	(105,64,39), #Reddish brown
	(207,96,36), #Flame reddish orange
	(163,162,164), #Medium stone grey
	(70,103,164), #Royal blue
	(35,71,139), #Dark Royal blue
	(142,66,133), #Bright reddish lilac
	(99,95,97), #Dark stone grey
	(130,138,93), #Lemon metalic
	(229,228,222), #Light stone grey
	(176,142,68), #Dark Curry
	(112,149,120), #Faded green
	(121,181,181), #Turquoise
	(159,195,233), #Light Royal blue
	(108,129,183), #Medium Royal blue
	(143,76,42), #Rust
	(124,92,69), #Brown
	(150,112,159), #Reddish lilac
	(107,98,155), #Lilac
	(167,169,206), #Light lilac
	(205,98,152), #Bright purple
	(228,173,200), #Light purple
	(220,144,149), #Light pink
	(240,213,160), #Light brick yellow
	(235,184,127), #Warm yellowish orange
	(253,234,140), #Cool yellow
	(125,187,221), #Dove blue
	(52,43,117), #Medium lilac
	(242,243,242), #White
]



class Lego(object):
	def __init__(self,number,name,RGBcolor,count):
		self.number = number 
		self.name = name 
		self.RGBcolor = RGBcolor 
		self.count = count

catalog = [
Lego (2,"Grey",(161,165,162),0),
Lego (3,"Light yellow",(249,233,153),0),
Lego (5,"Brick yellow",(215,197,153),0),
Lego (6,"Light green (Mint)",(194,218,184),0),
Lego (9,"Light reddish violet",(232,186,199),0),
Lego (12,"Light orange brown",(203,132,66),0),
Lego (18,"Nougat",(204,142,104),0),
Lego (21,"Bright red",(196,40,27),0),
Lego (22,"Med. reddish violet",(196,112,160),0),
Lego (23,"Bright blue",(13,105,171),0),
Lego (24,"Bright yellow",(245,205,47),0),
Lego (25,"Earth orange",(98,71,50),0),
Lego (26,"Black",(27,42,52),0),
Lego (27,"Dark grey",(109,110,108),0),
Lego (28,"Dark green",(40,127,70),0),
Lego (29,"Medium green",(161,196,139),0),
Lego (36,"Lig. Yellowich orange",(243,207,155),0),
Lego (37,"Bright green",(75,151,74),0),
Lego (38,"Dark orange",(160,95,52),0),
Lego (39,"Light bluish violet",(193,202,222),0),
Lego (40,"Transparent",(236,236,236),0),
Lego (41,"Tr. Red",(205,84,75),0),
Lego (42,"Tr. Lg blue",(193,223,240),0),
Lego (43,"Tr. Blue",(123,182,232),0),
Lego (44,"Tr. Yellow",(247,241,141),0),
Lego (45,"Light blue",(180,210,227),0),
Lego (47,"Tr. Flu. Reddish orange",(217,133,108),0),
Lego (48,"Tr. Green",(132,182,141),0),
Lego (49,"Tr. Flu. Green",(248,241,132),0),
Lego (50,"Phosph. White",(236,232,222),0),
Lego (100,"Light red",(238,196,182),0),
Lego (101,"Medium red",(218,134,121),0),
Lego (102,"Medium blue",(110,153,201),0),
Lego (103,"Light grey",(199,193,183),0),
Lego (104,"Bright violet",(107,50,123),0),
Lego (105,"Br. yellowish orange",(226,155,63),0),
Lego (106,"Bright orange",(218,133,64),0),
Lego (107,"Bright bluish green",(0,143,155),0),
Lego (108,"Earth yellow",(104,92,67),0),
Lego (110,"Bright bluish violet",(67,84,147),0),
Lego (111,"Tr. Brown",(191,183,177),0),
Lego (112,"Medium bluish violet",(104,116,172),0),
Lego (113,"Tr. Medi. reddish violet",(228,173,200),0),
Lego (115,"Med. yellowish green",(199,210,60),0),
Lego (116,"Med. bluish green",(85,165,175),0),
Lego (118,"Light bluish green",(183,215,213),0),
Lego (119,"Br. yellowish green",(164,189,70),0),
Lego (120,"Lig. yellowish green",(217,228,167),0),
Lego (121,"Med. yellowish orange",(231,172,88),0),
Lego (123,"Br. reddish orange",(211,111,76),0),
Lego (124,"Bright reddish violet",(146,57,120),0),
Lego (125,"Light orange",(234,184,145),0),
Lego (126,"Tr. Bright bluish violet",(165,165,203),0),
Lego (127,"Gold",(220,188,129),0),
Lego (128,"Dark nougat",(174,122,89),0),
Lego (131,"Silver",(156,163,168),0),
Lego (133,"Neon orange",(213,115,61),0),
Lego (134,"Neon green",(216,221,86),0),
Lego (135,"Sand blue",(116,134,156),0),
Lego (136,"Sand violet",(135,124,144),0),
Lego (137,"Medium orange",(224,152,100),0),
Lego (138,"Sand yellow",(149,138,115),0),
Lego (140,"Earth blue",(32,58,86),0),
Lego (141,"Earth green",(39,70,44),0),
Lego (143,"Tr. Flu. Blue",(207,226,247),0),
Lego (145,"Sand blue metallic",(121,136,161),0),
Lego (146,"Sand violet metallic",(149,142,163),0),
Lego (147,"Sand yellow metallic",(147,135,103),0),
Lego (148,"Dark grey metallic",(87,88,87),0),
Lego (149,"Black metallic",(22,29,50),0),
Lego (150,"Light grey metallic",(171,173,172),0),
Lego (151,"Sand green",(120,144,129),0),
Lego (153,"Sand red",(149,121,118),0),
Lego (154,"Dark red",(123,46,47),0),
Lego (157,"Tr. Flu. Yellow",(255,246,123),0),
Lego (158,"Tr. Flu. Red",(225,164,194),0),
Lego (168,"Gun metallic",(117,108,98),0),
Lego (176,"Red flip/flop",(151,105,91),0),
Lego (178,"Yellow flip/flop",(180,132,85),0),
Lego (179,"Silver flip/flop",(137,135,136),0),
Lego (180,"Curry",(215,169,75),0),
Lego (190,"Fire Yellow",(249,214,46),0),
Lego (191,"Flame yellowish orange",(232,171,45),0),
Lego (192,"Reddish brown",(105,64,39),0),
Lego (193,"Flame reddish orange",(207,96,36),0),
Lego (194,"Medium stone grey",(163,162,164),0),
Lego (195,"Royal blue",(70,103,164),0),
Lego (196,"Dark Royal blue",(35,71,139),0),
Lego (198,"Bright reddish lilac",(142,66,133),0),
Lego (199,"Dark stone grey",(99,95,97),0),
Lego (200,"Lemon metalic",(130,138,93),0),
Lego (208,"Light stone grey",(229,228,222),0),
Lego (209,"Dark Curry",(176,142,68),0),
Lego (210,"Faded green",(112,149,120),0),
Lego (211,"Turquoise",(121,181,181),0),
Lego (212,"Light Royal blue",(159,195,233),0),
Lego (213,"Medium Royal blue",(108,129,183),0),
Lego (216,"Rust",(143,76,42),0),
Lego (217,"Brown",(124,92,69),0),
Lego (218,"Reddish lilac",(150,112,159),0),
Lego (219,"Lilac",(107,98,155),0),
Lego (220,"Light lilac",(167,169,206),0),
Lego (221,"Bright purple",(205,98,152),0),
Lego (222,"Light purple",(228,173,200),0),
Lego (223,"Light pink",(220,144,149),0),
Lego (224,"Light brick yellow",(240,213,160),0),
Lego (225,"Warm yellowish orange",(235,184,127),0),
Lego (226,"Cool yellow",(253,234,140),0),
Lego (232,"Dove blue",(125,187,221),0),
Lego (268,"Medium lilac",(52,43,117),0),
Lego (1,"White",(242,243,242),0),
]
print (catalog[2].RGBcolor)

while len(palette) < 256:
    palette.append((0, 0, 0))

#PIL needs a flat array, not an array of tuples ß
# Next round: From python 3, Removed reduce(). Use functools.reduce() if you really need it; however, 99 percent of the time an explicit for loop is more readable.
flat_palette = functools.reduce(lambda a, b: a+b, palette)
assert len(flat_palette) == 768

#Declare an image to hold the palette 
palette_img = Image.new('P', (1, 1), 0)
palette_img.putpalette(flat_palette)

multiplier = 8#The higher the number the noisier the picture appears 
img = Image.open(input_path)

img = img.resize((size[0] * multiplier, size[1] * multiplier), Image.BICUBIC)
img = img.quantize(palette=palette_img) #reduce the palette

img = img.convert('RGB')

out = Image.new('RGB', size)
for x in range(size[0]):
    for y in range(size[1]):
        #sample at get average color in the corresponding square
        histogram = defaultdict(int)
        for x2 in range(x * multiplier, (x + 1) * multiplier):
            for y2 in range(y * multiplier, (y + 1) * multiplier):
                histogram[img.getpixel((x2,y2))] += 1
        color = max(histogram.keys(), key=operator.itemgetter(1))
        out.putpixel((x, y), color)
        for i in range(0,len(catalog)):
        	if catalog[i].RGBcolor == color: 
        		catalog[i].count += 1 



out= out.resize((440,600))
out.save(output_path)

print ("Shopping List")
for i in range(0,len(catalog)):
	if catalog[i].count > 0: 
		print (catalog[i].name,":",catalog[i].count)