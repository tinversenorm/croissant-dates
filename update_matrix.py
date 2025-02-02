import json
import sys

def read_json(filename):
	with open(filename, 'r') as file:
		return json.load(file)

def main():
	round_records = read_json('rounds.json')
	dry_run = True
	if len(sys.argv) > 1 and sys.argv[1] == 'write':
		dry_run = False

	names = set()

	# Go through the records once to get all the names.
	for round_rec in round_records:
		# Add the names to the list of all names
		for key in round_rec.keys():
			names.add(key)
			for val in round_rec[key]:
				names.add(val)

	# Build the matrix with zeros.
	matrix = {}
	names_list = list(names)
	for i in range(0, len(names_list)):
		for j in range(0, len(names_list)):
			if names_list[i] not in matrix:
				matrix[names_list[i]] = {}
			matrix[names_list[i]][names_list[j]] = 0 

	# Go through the records again to build the matrix with scores.
	# We're going backwards through the records this time.
	rounds_ago = 1
	for round_index in range(len(round_records) - 1, 0, -1):
		current_round = round_records[round_index]

		# Calculate a "score" used to reduce matching with people too recently.
		score = 0
		if rounds_ago < 100:
			score = 100 - rounds_ago

		for name in current_round.keys():
			for name2 in current_round[name]:
				matrix[name][name2] = score
				matrix[name2][name] = score

		# Increment the round counter.
		rounds_ago += 1

	if not dry_run:
		with open('previous_matches_matrix.json', 'w') as file:
			json.dump(matrix, file, indent=4)
	else:
		print(matrix)

if __name__ == '__main__':
	main()
