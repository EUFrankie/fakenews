import unittest
from application.text_checker.frankie_server_interface import FrankieZmqServer
import zmq

class TestZmqServer(unittest.TestCase):

  def setUp(self):
    self.server = FrankieZmqServer(time_out=1000)
    try:
      self.server.request_embedding("Some Test String to assure Server is running")
    except zmq.error.Again:
      self.skipTest("ZMQ Server is not running (timeout). Will skip interface test")


  def test_request_embedding(self):
    out = self.server.request_embedding("Some Test String to test general embedding format")
    self.assertEqual(len(out), 1)
    self.assertEqual(len(out[0]), 768)

  def test_request_multiple_embeddings(self):
    query_list = [
      "First Test String to test multi embedding format",
      "Second Test String to test multi embedding format",
      "Third Test String to test multi embedding format",
      "Fourth Test String to test multi embedding format",
      "Fifth Test String to test multi embedding format"
    ]
    out = self.server.request_multiple_embeddings(query_list)
    self.assertEqual(len(out), 5)
    for i in range(5):
      self.assertEqual(len(out[i]), 768)


if __name__ == '__main__':
    unittest.main()