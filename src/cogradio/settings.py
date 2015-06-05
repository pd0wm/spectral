class Settings(object):

    def __init__(self, web_opt, src_opt, rec_opt, det_opt):
        self.queues = [web_opt, src_opt, rec_opt, det_opt]

    def update(self, update):
        [self.send(queue, update) for queue in self.queues]

    def send(self, queue, update):
        if queue.full():
            queue.get()
        queue.put_nowait(update)
