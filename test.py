import unittest

from anime_downloader import parse_episodes_list


class TestStringMethods(unittest.TestCase):
    def test_parse_episodes_list_only_commas(self):
        self.assertEqual(parse_episodes_list(["1,3,7,12"]), [1,3,7,12])

    def test_parse_episodes_list_mixed_spaces_commas(self):
        self.assertEqual(parse_episodes_list(['1,', '3,', '7', '12']), [1,3,7,12])

    def test_parse_episodes_list_only_spaces(self):
        self.assertEqual(parse_episodes_list(['1', '3', '7']), [1,3,7])

    def test_parse_episodes_list_bounded(self):
        self.assertEqual(parse_episodes_list(['1-7,10'],12), [1,2,3,4,5,6,7,10])

    def test_parse_episodes_list__right_unbounded(self):
        self.assertEqual(parse_episodes_list(['3,9-'],12), [3,9,10,11,12])

    def test_parse_episodes_list__left_unbounded(self):
        self.assertEqual(parse_episodes_list(['8,-5'],12), [1,2,3,4,5,8])

if __name__ == '__main__':
    unittest.main()