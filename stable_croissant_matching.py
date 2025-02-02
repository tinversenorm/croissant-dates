#
#  stable_croissant_matching.py uses the Stable Roommate algorithm to match people into pairs for croissant dates.
#   
#  It uses the `rounds.json` file, which tracks previous matchings and should be up to date before running this script.
#  Add the names you would like to match for the current round in a list called `names_to_match.txt`
#
#  Run this script like this example:
#  
#  python3 stable_croissant_matching.py
#

import json
import random
import matching
import sys
import itertools
from matching.games import StableRoommates

def parse_names_list_from_args():
	lines = []
	with open('names_to_match.txt', 'r') as file:
		lines = file.readlines()
	names = []
	for line in lines:
		if line.strip() != "":
			names.append(line.strip())
	return names

def get_previous_rounds():
	rounds_json = []
	with open('rounds.json', 'r') as file:
	    rounds_json = json.load(file)

    # We need to go through each round and add all the names in the matching.
	for round_i in rounds_json:
		# Existing names in the round dict.
		existing_names = round_i.keys()
		additional_pairs = {}
		for key in existing_names:
			add_names = round_i[key]
			for name in add_names:
				if name not in additional_pairs.keys():
					additional_pairs[name] = []
				additional_pairs[name].append(key)

		round_i.update(additional_pairs)
	return rounds_json

# Take a round JSON and convert it to matrix with True indicating that the pair was matched.
def update_match_matrix(current_round: dict[str, list[str]], name_indices: dict[str, int], matrix: list[list[bool]]):
	size = len(name_indices)

	# Iterate through each pairing in the round.
	# Each pairing is a name -> [other, other2, ....]
	# We need to find all pairs of these names (n choose 2)
	# And input that pairing into the matrix.
	# If a name is unknown by `name_indices`, it doesn't need to be in the round.
	# That means we can ignore all 
	for name, matches in current_round.items():
		# Exclude any names we don't care about.
		all_names = [name] + matches
		relevant_names = [n for n in all_names if n in name_indices]

		combinations_n = len(relevant_names)
		combinations = [i for i in itertools.combinations(range(0, combinations_n), 2) if i[0] != i[1]]

		combination_indices = sorted([name_indices[n] for n in relevant_names])

		for i, j in combinations:
			# Combinations to input into the matrix.
			comb_i, comb_j = (combination_indices[i], combination_indices[j])
			matrix[comb_i][comb_j] = True
			matrix[comb_j][comb_i] = True

def create_preference_lists(previous_rounds: list[dict[str, list[str]]], names: list[str]):
	preferences = {}

	# Add all the names to the preferences list as keys.
	for name in names:
		preferences[name] = []

	# Used for figuring out which names are not matched.
	names_set = set(names)

	# Matches matrix for indicating who has already been matched.
	num_names = len(names)
	names_to_indices = {name:index for name, index in zip(names, range(num_names))}
	matched_matrix = [[False] * num_names for i in range(num_names)]

	# Iterate through the previous rounds in reverse order.
	for round_i in reversed(previous_rounds):
		# Add the matched name(s) in the previous round if that person is participating.
		update_match_matrix(round_i, names_to_indices, matched_matrix)

	# Construct the preference lists by finding all matched names and unmatched names in the list
	# of names we want to match.
	# The preference list should be = random ordering of unmatched names + random order of matched names
	for name in names:
		# Then, add the rest of the names to the preference list in random order.
		name_matches = matched_matrix[names_to_indices[name]]
		matched_names = set([names[i] for i, matched in enumerate(name_matches) if matched])
		unmatched_names = names_set.difference(matched_names)

		# Also remove their own name.
		unmatched_names = list(unmatched_names.difference(name))

		# Shuffle this list so the outcome of the algorithm is not deterministic.
		random.shuffle(unmatched_names)

        # Prepend the unmatched names to the preferences.
		preferences[name] = unmatched_names + list(matched_names)

		if name in preferences[name]:
			preferences[name].remove(name)

	return preferences

# Run the stable roommates algorithm to generate the best matchings.
def stable_roommates(names, preferences):
	# Create Players for matching algorithm.
	players = []
	name_to_players = {} # Match name to player for ease of access.
	for name in names:
		p = matching.Player(name)
		players.append(p)
		name_to_players[name] = p

	# Set the preferences of the players from the preferences dict.
	for name in name_to_players.keys():
		prefs = preferences[name]
		pref_players = []
		for p in prefs:
			pref_players.append(name_to_players[p])
		name_to_players[name].set_prefs(pref_players)

	game = StableRoommates(players)
	solution = game.solve()

	print("And the matches are....\n")
	matched = set()
	for first, second in solution.items():
		if first in matched and second in matched:
			continue
		matched.update([first, second])
		print(first, "and", second)


def main():
	names = parse_names_list_from_args()
	print("Names to match: ", names, "\n")

	previous_rounds = get_previous_rounds()
	print("Previous rounds: ", previous_rounds, "\n")

	preferences = create_preference_lists(previous_rounds, names)
	print("Preference lists: ", preferences, "\n")

	stable_roommates(names, preferences)

if __name__ == "__main__":
    main()
