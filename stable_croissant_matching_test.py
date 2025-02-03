import unittest
from stable_croissant_matching import create_preference_lists, update_match_matrix

class StableCroissantMatchingTest(unittest.TestCase):

	def test_match_matrix(self):
		previous_round = {
			"Gregory": ["Janine"],
			"Barbara": ["Ava"]
		}

		name_to_index = {
		    "Manny": 0,
			"Gregory" : 1,
			"Janine":  2,
			"Barbara" : 3
		}

		matrix = [[False] * 4 for i in range(4)]

		update_match_matrix(previous_round, name_to_index, matrix)

		self.assertEqual(
			matrix, 
			[[False, False, False, False], 
			[False, False, True, False],
			[False, True, False, False],
			[False, False, False, False]])

	def test_match_matrix_threepair(self):
		previous_round = {
			"Gregory": ["Janine"],
			"Barbara": ["Ava"],
			"Jacob": ["Avi", "Zach"]
		}

		name_to_index = {
		    "Manny": 0,
			"Gregory" : 1,
			"Janine" : 2,
			"Jacob" : 3,
			"Avi" : 4,
			"Zach" : 5
		}

		matrix = [[False] * 6 for i in range(6)]

		update_match_matrix(previous_round, name_to_index, matrix)

		self.assertEqual(
			matrix, 
			[[False, False, False, False, False, False], 
			[False, False, True, False, False, False],
			[False, True, False, False, False, False],
			[False, False, False, False, True, True],
			[False, False, False, True, False, True],
			[False, False, False, True, True, False]])


	def test_create_preference_lists(self):
		previous_rounds = [
		{
			"Gregory": ["Janine"],
			"Barbara": ["Ava"]
		}]

		names_to_match = ["Gregory", "Janine", "Ava", "Jacob"]

		pref_lists = create_preference_lists(previous_rounds, names_to_match)

		# Make sure the previous matches are at the end of the preference lists.
		self.assertEqual("Gregory", pref_lists["Janine"][-1])
		self.assertEqual("Janine", pref_lists["Gregory"][-1])


	def test_create_preference_lists_threepair(self):
		previous_rounds = [{
			"Gregory": ["Janine"],
			"Barbara": ["Ava"],
			"Jacob": ["Avi", "Zach"]
		}]

		names_to_match = ["Gregory", "Janine", "Ava", "Jacob", "Zach", "Avi"]

		pref_lists = create_preference_lists(previous_rounds, names_to_match)

		# Make sure the previous matches are at the end of the preference lists.
		self.assertEqual("Gregory", pref_lists["Janine"][-1])
		self.assertEqual("Janine", pref_lists["Gregory"][-1])
		self.assertCountEqual(["Avi", "Zach"], pref_lists["Jacob"][-2:])
		self.assertCountEqual(["Jacob", "Zach"], pref_lists["Avi"][-2:])
		self.assertCountEqual(["Avi", "Jacob"], pref_lists["Zach"][-2:])

if __name__ == '__main__':
    unittest.main()