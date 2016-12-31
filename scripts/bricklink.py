import argparse
import re
import csv
import xml.etree.ElementTree as xml
from xml.dom import minidom

class LegoPart:

	def __init__(self, id):
		self.id = id
		self.color = ""
		self.wanted = 0
		self.sets = []
		self.type = "?"
		
	def setColor(self, color):
		self.color = color

	def addSet(self, set):
		self.sets.append(set)
		
	def addWanted(self, count):
		self.wanted = self.wanted + count
		
	def setType(self, type):
		self.type = type
		
def parseOptions():
	parser = argparse.ArgumentParser()

	parser.add_argument('colorList', help='The list of colors for the lego parts')
	parser.add_argument('partList', help='The list of lego parts')
	parser.add_argument('--sep', dest='separatorChar', help='separator character')

	return parser.parse_args()

def load_colors(filename):
	color_list = {}
	with open(filename, encoding="utf8") as f:
		reader = csv.reader(f, delimiter='\t')
		next(reader, None)  # skip the headers
		next(reader, None)  # skip empty line
		for row in reader:
			color_id = row[0].strip()
			color_name = row[1].lower().strip()
			color_list [color_name] = color_id
			
	return color_list

def load_parts(filename, separator, part_list):
	with open(filename, encoding="utf8") as f:
		reader = csv.reader(f, delimiter=separator)
		next(reader, None)  # skip the headers
		for row in reader:
			setId = re.sub('[^0-9a-zA-Z]+', '', row[0])
			partCount = int (re.sub('[^0-9a-zA-Z]+', '', row[1]))
			partId = re.sub('[^0-9a-zA-Z]+', '', row[2])
			partColor = re.sub('[^0-9a-zA-Z -]+', '', row[3].lower())
			partType = re.sub('[^0-9a-zA-Z]+', '', row[4])

			key = (partId, partColor)
			
			if key in part_list:
				legoPart = part_list[key]
				legoPart.addWanted(partCount)
				legoPart.addSet(setId)
			else:
				legoPart = LegoPart(partId)
				legoPart.setColor(partColor)
				legoPart.setType(partType)
				legoPart.addWanted(partCount)
				legoPart.addSet(setId)
				
				part_list [key] = legoPart

def determine_color(part_color, color_list):

	color_error_count = 0
	color_id = ""
	
	if part_color not in color_list and part_color != "nvt":
		print ("Color '%s' not supported" % part_color)
		color_error_count = color_error_count + 1
	else:
		if part_color == "nvt":
			color_id = 0
		else:
			color_id = color_list[part_color]
	return color_id
				
def write_xml(filename, part_list, color_list):
	inventory = xml.Element('INVENTORY')
	
	partId = ""
	partColor = ""
	key = (partId, partColor)
	for key in part_list:
	
		legoPart = part_list[key]
		
		item = xml.Element('ITEM')
	
		itemType = xml.Element('ITEMTYPE')
		itemType.text = legoPart.type

		itemId = xml.Element('ITEMID')
		itemId.text = str(legoPart.id)
	
		color = xml.Element('COLOR')
		color.text = str(determine_color(legoPart.color, color_list))
	
		minQuantity = xml.Element('MINQTY')
		minQuantity.text = str(legoPart.wanted)
	
		item.append(itemType)
		item.append(itemId)
		item.append(color)
		item.append(minQuantity)
	
		inventory.append(item)
	
	xmlstr = minidom.parseString(xml.tostring(inventory)).toprettyxml(indent="  ")
	with open("test.xml", "w") as f:
		f.write(xmlstr)
	
#	tree = xml.ElementTree(inventory)
#	tree.write("test.xml")

				
def main():
	args = parseOptions()

	part_list = {}
	colors = {}
	
	colors = load_colors(args.colorList)
	load_parts(args.partList, args.separatorChar, part_list)
	
	write_xml("output.xml", part_list, colors)
	
	
	print (len(part_list))
	
if __name__ == "__main__":
    main()
