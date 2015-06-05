class Settings(object):

    def __init__(self):
        self.options = dict()

        if not self.opt.empty():
            options = self.opt.get()
    def update(self, update):
        self.options.update(update)

    def read(self):
        return self.options

