from queue import Queue
from gpt4all import GPT4All
from threading import Thread

in_queue=None
out_queue=None

class ModelThread():
    isRunning=False
    in_queue = None
    out_queue = None
    thread = None
    model = None 
    role = None

    def InitThread(self, in_queue, out_queue):
        self.in_queue = in_queue
        self.out_queue = out_queue

    def initModel(self, model_name, role=None): 
        self.model = GPT4All(model_name)
        self.role = role

    def changeRole(self, role):
        self.role = role

    def startThread(self):
        self.thread = Thread(target=worker, args=(self.model, self.role, self.in_queue, self.out_queue,))
        self.thread.start()
        self.isRunning = True


# Object that signals shutdown
_sentinel = object()
    
def worker(model, role, in_q, out_q):
    with model.chat_session(role['system_prompt'], role['prompt_template']):
        for data in iter(in_q.get, _sentinel):
            if data == "/reset":
                break
            output = model.generate(data)
            out_q.put(output)
