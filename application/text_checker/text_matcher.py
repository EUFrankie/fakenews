import pandas as pd
import scipy
import numpy as np
from ast import literal_eval
from frankie_ai.models.FrankieSentenceEncoder import FrankieSentenceEncoder
from frankie_ai.datasets.STSBenchmark import STSBenchmarkDatasetForEncoding

# Init global variables
encoder = None
corpus_df = None
corpus_embeddings = None
closest_n = 3

def init_text_matcher():
  global encoder, corpus_df, corpus_embeddings
  if encoder is None:
    encoder = FrankieSentenceEncoder(
      STSBenchmarkDatasetForEncoding,
      weights_path="/home/jan/frankie-ai/.trained_models/frankie_encoder/ec.ckpt"
    )
    print("Initialized Encoder")

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


def find_best_matches(query):
  query_embedding = encoder.encode([query])
  distances = scipy.spatial.distance.cdist(query_embedding, corpus_embeddings, "cosine")[0]
  results = zip(range(len(distances)), distances)
  results = sorted(results, key=lambda x: x[1])
  output_list = []

  for idx, distance in results[0:closest_n]:
    relevant_row = corpus_df.iloc[idx]
    output_list.append({
      "fact_checker": relevant_row.fact_checker,
      "date": relevant_row.date,
      "location": relevant_row.location,
      "label": relevant_row.label,
      "title": relevant_row.title,
      "explanation": relevant_row.explanation,
      "url_checker": relevant_row.url_checker,
      "score": 1-distance
    })

  return output_list

if __name__ == "__main__":
  init_text_matcher()
  out = find_best_matches("COVID-19 was created in a chinese lab")
  print(out)