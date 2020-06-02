import pandas as pd
import scipy.spatial
import numpy as np
import zmq
import os

context = zmq.Context()

#  Socket to talk to server
print("Connecting to frankie ai server…")
socket = context.socket(zmq.REQ)
address = os.getenv('SERVER_ADDRESS', '127.0.0.1:5555')
print("Address: " + address)
socket.connect("tcp://" + address)

# Init global variables
corpus_df = None
corpus_embeddings = None
closest_n = 3

def init_text_matcher():
  global corpus_df, corpus_embeddings


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

def _request_embedding(query):
  request = str.encode(query)
  socket.send(request)
  response = socket.recv_json()
  return response

def find_best_matches(query):
  query_embedding = _request_embedding(query)
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
      "score": int((1-distance)*100)
    })

  return output_list

def find_one_best_match(query):
  query_embedding = _request_embedding(query)
  distances = scipy.spatial.distance.cdist(query_embedding, corpus_embeddings, "cosine")[0]
  results = zip(range(len(distances)), distances)
  results = sorted(results, key=lambda x: x[1])
  
  idx, distance = results[0]
  relevant_row = corpus_df.iloc[idx]

  return {
    "fact_checker": relevant_row.fact_checker,
    "date": relevant_row.date,
    "location": relevant_row.location,
    "label": relevant_row.label,
    "title": relevant_row.title,
    "explanation": relevant_row.explanation,
    "url_checker": relevant_row.url_checker,
    "score": int((1-distance)*100)
  }

if __name__ == "__main__":
  init_text_matcher()
  out = find_best_matches("COVID-19 was created in a chinese lab")
  print(out)