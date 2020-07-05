import zmq, os

class FrankieServerInterface:

  def request_embedding(self, query):
    pass

  def request_multiple_embeddings(self, query_list):
    pass

class FrankieZmqServer(FrankieServerInterface):

  def __init__(self, time_out=None):
    self.context = zmq.Context()

    # Set timeout of connection to avoid infinite wait
    if time_out:
      self.context.setsockopt(zmq.RCVTIMEO, time_out)


    #  Socket to talk to server
    print("Connecting to frankie ai server…")
    self.socket = self.context.socket(zmq.REQ)
    self.address = os.getenv('SERVER_ADDRESS', '127.0.0.1:5555')
    print("Address: " + self.address)
    self.socket.linger = 250
    self.socket.connect("tcp://" + self.address)

  def request_embedding(self, query):
    return self.request_multiple_embeddings([query])


  def request_multiple_embeddings(self, query_list):
    self.socket.send_json(query_list)
    response = self.socket.recv_json()
    return response
