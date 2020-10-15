import pandas as pd
import scipy.spatial
import numpy as np
from application.text_checker.frankie_server_interface import FrankieServerInterface

# Init global variables
corpus_df = None
corpus_embeddings = None
closest_n = 3
frankie_server = None

def init_text_matcher(server: FrankieServerInterface):
  global corpus_df, corpus_embeddings, frankie_server

  frankie_server = server
  if corpus_df is None or corpus_embeddings is None:
    corpus_df = pd.read_csv('data/fact_check_data_incl_encodings.csv')
    corpus_df = corpus_df[corpus_df.title.str.split().apply(lambda x: len(x) >= 3)]
    # TODO Find better method to store encodings
    # The following lines were used to create embeddings in npy file
    # conv_lists = corpus_df.encoding.apply(literal_eval)
    # corpus_embeddings = np.array(conv_lists.to_list())
    with open("data/corpus_embeddings.npy", 'rb') as f:
      corpus_embeddings = np.load(f, corpus_embeddings)

    print("Embeddings Shape: " + str(corpus_embeddings.shape))
    print("Initialized Corpus of size: " + str(corpus_df.shape[0]))

def _relevant_row_to_dict(relevant_row, score):
  return {
      "fact_checker": relevant_row.fact_checker,
      "date": relevant_row.date,
      "location": relevant_row.location,
      "label": relevant_row.label,
      "title": relevant_row.title,
      "explanation": relevant_row.explanation,
      "url_checker": relevant_row.url_checker,
      "score": score
    }

def _create_output_list(results, n):
  output_list = []

  for idx, distance in results[0:n]:
    relevant_row = corpus_df.iloc[idx]
    output_list.append(_relevant_row_to_dict(relevant_row, _distance_to_score(distance)))

  return output_list

def _prepare_results(distances):
  results = zip(range(len(distances)), distances)
  return sorted(results, key=lambda x: x[1])

def _distance_to_score(distance):
  return int((1 - distance) * 100)

def best_matches(query, number_of_matches = None):
  if number_of_matches == None:
    number_of_matches = closest_n
  query_embedding = frankie_server.request_embedding(query)
  distances = scipy.spatial.distance.cdist(query_embedding, corpus_embeddings, "cosine")[0]
  results = _prepare_results(distances)

  return _create_output_list(results, number_of_matches)

def random_matches():
  n = 10
  indizes = np.random.randint(corpus_df.shape[0], size=n)
  distances = np.zeros(n)
  results = _prepare_results(distances)

  return _create_output_list(results, 10)

def matches_with_score_higher_than(score, query):
  query_embedding = frankie_server.request_embedding(query)
  distances = scipy.spatial.distance.cdist(query_embedding, corpus_embeddings, "cosine")[0]
  results = _prepare_results(distances)

  output_list = []

  for idx, distance in results:
    calculated_score = _distance_to_score(distance)

    if calculated_score > score:
      relevant_row = corpus_df.iloc[idx]
      output_list.append( _relevant_row_to_dict(relevant_row, calculated_score))
    else:
      # Since the results are sorted based on the score we can break as soon as one score is lower than
      # the target score.
      break

  return output_list

def one_best_match(query):
  query_embedding = frankie_server.request_embedding(query)
  distances = scipy.spatial.distance.cdist(query_embedding, corpus_embeddings, "cosine")[0]
  results = _prepare_results(distances)
  
  idx, distance = results[0]
  relevant_row = corpus_df.iloc[idx]

  return  _relevant_row_to_dict(relevant_row, _distance_to_score(distance))

def list_matches(query_list, corpus_list):
  query_embeddings = frankie_server.request_multiple_embeddings(query_list)
  local_corpus_embeddings = frankie_server.request_multiple_embeddings(corpus_list)
  distances_all = scipy.spatial.distance.cdist(query_embeddings, local_corpus_embeddings, "cosine")

  match_list = list()
  for query_idx in range(distances_all.shape[0]):
    distances = distances_all[query_idx]
    results = _prepare_results(distances)
    idx, distance = results[0]
    match_list.append({
      "sentence": corpus_list[idx],
      "corpus_index": idx,
      "score": _distance_to_score(distance)
    })

  return match_list

if __name__ == "__main__":
  init_text_matcher()
  out = best_matches("COVID-19 was created in a chinese lab")
  print(out)