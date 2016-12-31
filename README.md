# lego
## Introduction
As a kid I had quite a few lego sets to play with. One day cleaning up the attic I came acros these lego set and decides to build all of them. As expected I was missing a few parts and wanted to buy the missing parts. I created and excel file containing all the missing
parts. Bricklink is a great place to buy all the missing parts but it is a daunting task to enter all the parts in the wishlist.
When I discovered that there is a possibility to mass upload all the parts using an XML file I decided to write a script to convert
the excel list into the xml file so that it can be uploaded to Bricklink.

This repository contains scripts to parse, convert and create lego parts lists.

##Usage
### mismatchedparts.py
1. Save the wanted_list.xlsx file as a csv file
1.Run the python script mismatchedparts.py with the following command
` python mismatchedparts.py refList wantedList`

### bricklink.py
1. Save the wanted_list.xlsx file as a csv file
1. Run the python script bricklink.py with the following command
`python bricklink.py --sep ; lego_colors.tsf wanted_list.csv`


