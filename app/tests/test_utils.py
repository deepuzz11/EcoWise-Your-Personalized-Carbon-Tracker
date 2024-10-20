import unittest
from app.utils import calculate_carbon_footprint

class UtilsTest(unittest.TestCase):

    def test_calculate_carbon_footprint(self):
        activities = [{'emissions': 10}, {'emissions': 20}]
        total_footprint = calculate_carbon_footprint(activities)
        self.assertEqual(total_footprint, 30)

if __name__ == '__main__':
    unittest.main()
