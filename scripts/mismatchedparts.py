import csv
import argparse
import re


def parseOptions():
	parser = argparse.ArgumentParser()

	parser.add_argument('refList', help='The reference list to find the mismatches in')
	parser.add_argument('matchList', help='The list to be matched with the reference list')

	return parser.parse_args()

	

def load_reference_list(reference):
	ref_list = []
	with open(reference, encoding="utf8") as f:
		reader = csv.reader(f, delimiter='\t')
		next(reader, None)  # skip the headers
		for row in reader:
			ref_list.append(row[2].lstrip())
	return ref_list

def load_match_list(matcher):
	match_list = []
	with open(matcher) as f:
		reader = csv.reader(f, delimiter=',')
		next(reader, None)  # skip the headers
		for row in reader:
			s = re.sub('[^0-9a-zA-Z]+', '', row[2])
			match_list.append(s)
	return match_list

	
def determine_mismatch(ref_list, match_list):
	found_list = []
	missing_list = []
	for part in match_list:
		if part in ref_list:
			found_list.append(part)
		else:
			missing_list.append(part)
	return missing_list

def print_mismatch_list(missing_list):
	print ("------------")
	print (" nr items missing = %d" % (len(missing_list)))
	print ("------------")
	print ("Items that are in wanted list but not in bricklink list:")
	for part in missing_list:
		print (part)
	print ("------------")

def main():
	args = parseOptions()
	bricklink_list = []
	wanted_list = []
	bricklink_list = load_reference_list(args.refList)
	wanted_list = load_match_list(args.matchList)
	missing_list = determine_mismatch(bricklink_list, wanted_list)
	print_mismatch_list(missing_list)
	
if __name__ == "__main__":
    main()
