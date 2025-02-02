# Update on each run.
current = ["zach", "Russell", "Kelvin", "Pranav", "Cat Nguyen", "Denalex", "ankil", "pooja", "ker lee", "cynthia", "jamie", "Di", "Christina P"]

import json
import random

def get_previous_matches():
	with open('previous_matches.json', 'r') as file:
	    return json.load(file)

def update_matches(previous_matches, new_match_tuples):
	data = previous_matches
	for pair in new_match_tuples:
	    key = pair[0]
	    val = pair[1]
	    # Add key -> val
	    if key in data:
	     	if val not in data[key]:
	     		data[key].append(val)
	    else:
	     	data[key] = [val]
	    # Add val -> key
	    if val in data:
	     	if key not in data[val]:
	     		data[val].append(key)
	    else:
	     	data[val] = [key]
	print("Updated JSON: ")
	print(json)
	with open('previous_matches2.json', 'w') as file:
	    json.dump(data, file, indent=4)
	    return data

def match(names, data):
	tuples = []
	names_iter = names.copy()
	random.shuffle(names_iter)
	while len(names_iter) > 2:
		first_name = names_iter[0]
		second_name = ""

		# Find the second name to pair with. It should be new.
		for name in names_iter[1:]:
			if name not in data[first_name]:
				# Found.
				second_name = name
				break

		# Unable to find a second name.
		if second_name == "":
			print("Failed to successfully match {n}... Try again.".format(n = first_name))
			break
		else:
			tuples.append((first_name, second_name))
			names_iter.remove(first_name)
			names_iter.remove(second_name)

	if len(names_iter) == 1:
		tuples[-1] = (tuples[-1][0], tuples[-1][1], names_iter[0])
	elif len(names_iter) == 2:
	    tuples.append((names_iter[0], names_iter[1]))		

	print(tuples)
	print(names_iter)

match(current, get_previous_matches())
