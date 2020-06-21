import unittest
from application.text_checker.text_matcher import find_random_matches, init_text_matcher

class TestTextMatcher(unittest.TestCase):

  def setUp(self):
    init_text_matcher()

  def test_result_not_nan(self):
    results = find_random_matches()
    for result in results:
      self.assertTrue(len(result['fact_checker']) > 0)

if __name__ == '__main__':
    unittest.main()