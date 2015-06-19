from multiprocessing import Queue, Lock

class SafeQueue:
    """ Safe Queue implementation is a wrapper around standard multiprocessing
        queue. Implements safe queuing and dequeueing. """

    def __init__(self, size=10):
        self._queue = Queue(size)
        self._lock = Lock()

    def queue(self, inp):
        self._lock.acquire()
        if self._queue.full():
            self._queue.get()
        self._queue.put_nowait(inp)
        self._lock.release()

    def dequeue(self):
        self._lock.acquire()
        item = None
        if not self._queue.empty():
            item = self._queue.get_nowait()
        self._lock.release()
        return item

