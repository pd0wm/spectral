class Settings(object):

    def __init__(self, web_opt, src_opt, rec_opt, det_opt):
        self.pipes = [web_opt, src_opt, rec_opt, det_opt]

    def update(self, update):
        [pipe.send(update) for pipe in self.pipes]
