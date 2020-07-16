import unittest
from application.text_checker.text_matcher import *
from application.text_checker.frankie_server_interface import FrankieServerInterface
import numpy as np
import pandas as pd

class FrankieServerMock(FrankieServerInterface):

  def __init__(self):
    with open("data/corpus_embeddings.npy", 'rb') as f:
      self.corpus_embeddings = np.load(f)

  def request_embedding(self, query):
    # Simply always return the first embedding
    return [self.corpus_embeddings[0]]

  def request_multiple_embeddings(self, query_list):
    # Simply return first n embeddings
    return self.corpus_embeddings[0:len(query_list)]


class TestTextMatcher(unittest.TestCase):

  def setUp(self):
    init_text_matcher(FrankieServerMock())
    self.corpus_df = pd.read_csv('data/fact_check_data_incl_encodings.csv')
    self.corpus_df = self.corpus_df[self.corpus_df.title.str.split().apply(lambda x: len(x) >= 3)]

  def test_result_not_nan(self):
    results = random_matches()
    for result in results:
      self.assertTrue(len(result['fact_checker']) > 0)

  def test_best_match(self):
    test_query = self.corpus_df.iloc[0].title
    results = best_matches(test_query)
    self.assertTrue(results[0]['title'] == test_query)

  def test_one_best_match(self):
    test_query = self.corpus_df.iloc[0].title
    results = one_best_match(test_query)
    self.assertTrue(results['title'] == test_query)

  def test_list_matches(self):
    corpus_list = self.corpus_df.iloc[0:20].title.to_list()
    query_list = self.corpus_df.iloc[0:5].title.to_list()
    matches = list_matches(query_list, corpus_list)
    self.assertTrue(matches is not None)
    for idx in range(len(matches)):
      match = matches[idx]
      self.assertEqual(match["sentence"], corpus_list[idx])
      self.assertGreaterEqual(match["score"], 99)
      self.assertGreaterEqual(match["corpus_index"], idx)


if __name__ == '__main__':
    unittest.main()