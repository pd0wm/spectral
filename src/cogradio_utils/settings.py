class Settings(object):

    def __init__(self, web_opt):
        self.web_opt = web_opt

    def update(self, update):
        self.web_opt.send(update)
