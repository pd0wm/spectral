class Detector(object):

    """Detector parent object"""

    def __init__(self):
        print("init")

    def detect(self, rx):
        raise NotImplementedError("Implement this method.")
