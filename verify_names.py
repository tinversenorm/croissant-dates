#
#
# verify_names.py checks to see if the names provided have been used before.
#
#
#

from difflib import get_close_matches
import json

def parse_names_list_from_args():
	lines = []
	with open('names_to_match.txt', 'r') as file:
		lines = file.readlines()
	names = []
	for line in lines:
		if line.strip() != "":
			names.append(line.strip())
	return names


def extract_known_names():
	# The data we store is in rounds.json
	rounds_json = []
	with open('rounds.json', 'r') as file:
		rounds_json = json.load(file)

	# We need to go through each round and add all the names in the matching.
	known_names = set()
	for round_i in rounds_json:
		# name_key is one person in a date, and name_values are the others.
		for name_key, name_values in round_i.items():
			known_names.add(name_key)
			known_names.update(name_values)

	print("Known names: ", known_names)
	print()
	return known_names

def verify_names():
	names_to_verify = parse_names_list_from_args()
	known_names = list(extract_known_names())

	for name in names_to_verify:
		most_similar_names = get_close_matches(name, known_names)
		if len(most_similar_names) > 0:
			print(f'{name} might be known, since it similar to {most_similar_names}')
		else:
			print(f'{name} is unknown!')


if __name__ == "__main__":
	verify_names()