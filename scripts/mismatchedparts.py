import csv
import argparse


parser = argparse.ArgumentParser()

parser.add_argument('refList', help='The reference list to find the mismatches in')
parser.add_argument('matchList', help='The list to be matched with the reference list')

args = parser.parse_args()

bricklink_partlist = []
wanted_partlist = []

with open(args.refList, encoding="utf8") as f:
	reader = csv.reader(f, delimiter='\t')
	for row in reader:
		bricklink_partlist.append(row[2])
		
		
with open(args.matchList) as f:
	reader = csv.reader(f, delimiter=',')
	for row in reader:
		wanted_partlist.append(row[2])
		
found_list = []
missing_list = []

for part in wanted_partlist:
	if part in bricklink_partlist:
		found_list.append(part)
	else:
		missing_list.append(part)

		
print ("------------")
print (" nr items found = %d" % (len(found_list)))
print (" nr items missing = %d" % (len(missing_list)))
print ("------------")
print ("Items that are in wanted list but not in bricklin list:")
for part in missing_list:
	print (part)
print ("------------")


