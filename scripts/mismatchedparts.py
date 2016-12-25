import csv

bricklink_partlist = []
wanted_partlist = []

with open("bricklink_parts.txt", encoding="utf8") as f:
	reader = csv.reader(f, delimiter='\t')
	for row in reader:
		bricklink_partlist.append(row[2])
		
		
with open("wanted_parts.csv") as f:
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


