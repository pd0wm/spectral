class Detector(object):

    """Detector parent object"""

    def __init__(self):
        print("init")

    def detect(self, rx):
        """
        Function to be implemented by children of this class.

        Args:
            rx: The input autocorrelation of the signal.
        Returns:
            Array of booleans which represent either signal or no signal in a specific interval.
        """
        raise NotImplementedError("Implement this method.")
