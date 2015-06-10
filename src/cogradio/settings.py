class Settings(object):

    def __init__(self):
        self.options = dict()

    def update(self, update):
        self.options.update(update)

    def read(self):
        return self.options
