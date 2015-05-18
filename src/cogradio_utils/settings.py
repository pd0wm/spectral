class Settings(object):

    def __init__(self, web_opt, src_opt):
        self.web_opt = web_opt
        self.src_opt = src_opt

    def update(self, update):
        # self.web_opt.send(update)
        self.src_opt.send(update)
