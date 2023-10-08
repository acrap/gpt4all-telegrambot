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
        thread = Thread(target=worker, args=(model_name, role, self.in_queue, self.out_queue,))
        thread.start()
        self.isRunning = True

# Object that signals shutdown
_sentinel = object()

def return_default_role():
    role = dict()
    role = {'system_prompt':'You an helpful AI assistent and you behave like an AI research assistant. You use a tone that is technical and scientific. Below is our chat history, please continue the conversaion.',
                    'prompt_template':'### Instruction:\n{0}\n### Response:\n'}
    return role
    
def worker(model_name, role, in_q, out_q):
    model = GPT4All(model_name)
    if role is None:
        role = return_default_role()
    with model.chat_session(role['system_prompt'], role['prompt_template']):
        for data in iter(in_q.get, _sentinel):
            output = model.generate(data)
            out_q.put(output)
