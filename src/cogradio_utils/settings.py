class Settings(object):

    def __init__(self):
        pass

    def update(self, update):
        self.parameters = update
        print "Updated", update

    def get(self):
        return self.parameters
        print "I dun got"
