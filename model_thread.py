from queue import Queue
from gpt4all import GPT4All
from threading import Thread

in_queue=None
out_queue=None

class ModelThread():
    isRunning=False
    in_queue = None
    out_queue = None
    def InitThread(self, in_queue, out_queue):
        self.in_queue = in_queue
        self.out_queue = out_queue

    def initModel(self, model_name, role=None): 
        print(self)
        thread = Thread(target=worker, args=(model_name, self.in_queue, self.out_queue,))
        thread.start()
        self.isRunning = True

# Object that signals shutdown
_sentinel = object()

def worker(model_name, in_q, out_q):
    model = GPT4All(model_name)
    for data in iter(in_q.get, _sentinel):
        output = model.generate(data)
        out_q.put(output)
