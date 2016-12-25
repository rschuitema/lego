import os.path
from collections import OrderedDict

lego_colors_filename = 'lego_colors.tsf'
lego_colors_separator = '\t'
lego_parts_filename = 'wanted_parts.csv'
lego_parts_separator = ','
bricklink_wishlist_filename = "bricklink.xml"
website_filename = "index.html"

def load_lego_colors ():
    input_file = open (lego_colors_filename, "r") 
    input_file.readline ()
    input_file.readline ()

    lego_colors = {}
    for line in input_file.readlines ():
        cols = line.split (lego_colors_separator)
        color_id = cols [0].strip ()
        color_name = cols [1].lower ().strip ()
        lego_colors [color_name] = color_id

    return lego_colors

def load_lego_parts ():
    input_file = open (lego_parts_filename, "r") 
    input_file.readline ()

    lego_parts = {}
    key_list = []
    for line in input_file.readlines ():
        cols = line.split (lego_parts_separator)
        part_id = cols [2].strip ()
        part_color = cols [3].lower ().strip ()
        part_count = int (cols [1].strip ())
        set_id = cols [0].strip ()
        key = (part_id, part_color)
        key_list.append (key)

        if key in lego_parts:
            lego_parts [key]["count"] = lego_parts [key]["count"] + part_count
            lego_parts [key]["sets"].append (set_id)
        else:
            lego_parts [key] = {"count": part_count, "sets" : [set_id]}

    key_list.sort ()

    sorted_parts = OrderedDict ({})
    for key in key_list:
        sorted_parts[key] = lego_parts[key]

    return sorted_parts

def generate_bricklink_wishlist (lego_colors, lego_parts):
    output_file = open (bricklink_wishlist_filename, "w")
    output_file.write ("<INVENTORY>\n")
    color_error_count = 0

    for part_id, part_color in lego_parts:
        if part_color not in lego_colors and part_color != "nvt":
            print ("Color '%s' not supported" % part_color)
            color_error_count = color_error_count + 1
        else:
            if part_color == "nvt":
                color_id = 0
            else:
                color_id = lego_colors[part_color]
            output_file.write ("\t<ITEM>\n")
            output_file.write ("\t\t<ITEMTYPE>P</ITEMTYPE>\n")
            output_file.write ("\t\t<ITEMID>%s</ITEMID>\n" % part_id)
            output_file.write ("\t\t<COLOR>%s</COLOR>\n" % color_id)
            part_count = lego_parts [(part_id, part_color)]["count"]
            output_file.write ("\t\t<MINQTY>%d</MINQTY>\n" % part_count)
            output_file.write ("\t</ITEM>\n")

    if (color_error_count > 0):
        print ("%d color(s) not found!" % color_error_count)

    output_file.write ("</INVENTORY>\n")
    output_file.close ()

def find_part_filename (part_id):
    filename = "../parts/%s.jpg" % part_id
    if not os.path.exists (filename):
       filename = "../parts/%s.gif" % part_id
       if not os.path.exists (filename):
           filename = "../parts/%s.png" % part_id
           if not os.path.exists (filename):
               filename = "-"

    return filename
    
def generate_website (lego_colors, lego_parts):
    output_file = open (website_filename, "w")
    output_file.write ('<HTML><BODY WIDTH="90%">\n')
    output_file.write ('\t<TABLE border="1">\n')
    output_file.write ('\t\t<TR><TD>Part Id</TD><TD>Color</TD><TD>Count</TD><TD>Image</TD><TD>Set-Ids</TD></TR>')
    no_image_error_count = 0
    total_part_count = 0
    for part_id, part_color in lego_parts:
        output_file.write ("\t\t<TR>")
        output_file.write ("<TD>%s</TD>" % part_id)
        output_file.write ("<TD>%s</TD>" % part_color)
        part_count = lego_parts[(part_id, part_color)]["count"]
        total_part_count = total_part_count + part_count
        output_file.write ("<TD>%d</TD>" % part_count)
        part_filename = find_part_filename (part_id)
        if part_filename != "-":
            output_file.write ('<TD><IMG HEIGHT="50" SRC="%s"></TD>' % part_filename)
        else:
            print ("Part '%s' does not have an image" % part_id)
            output_file.write ('<TD>No Image</TD>')
            no_image_error_count = no_image_error_count + 1

        output_file.write ("<TD>")
        for set_id in lego_parts [(part_id, part_color)]["sets"]:
            output_file.write ("%s<BR/>" % set_id)
        output_file.write ("</TD>")
        output_file.write ("\t\t</TR>\n")

    print ("%d parts don't have an image" % no_image_error_count)
    output_file.write ("\t</TABLE>\n\n")
    output_file.write ("Total bricks to buy: %d\n" % total_part_count)
    output_file.write ("</BODY></HTML>\n")
    output_file.close ()


lego_colors = load_lego_colors ()
lego_parts = load_lego_parts ()

generate_bricklink_wishlist (lego_colors, lego_parts)
generate_website (lego_colors, lego_parts)
