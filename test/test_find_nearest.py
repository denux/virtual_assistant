import unittest
import json
from utils.find_nearest import FindNearest
import os

with open(os.getenv("config_json_path", ""), "rb") as f:
    config_json = json.load(f)


class TestNearestMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.find_nearest = FindNearest(config_json.get("find_nearest"))

    def test_gym(self):
        command = "find nearest gym"
        entity = self.find_nearest.get_entity(command)
        list_places = self.find_nearest.get_search_results(entity)
        self.assertEqual(len(list_places), 5)


if __name__ == '__main__':
    unittest.main()


