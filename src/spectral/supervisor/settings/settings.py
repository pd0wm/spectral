class Settings(object):
    """
    Observer object for the settings. Maintains a dictionary with key value pairs
    for settings.
    """
    def __init__(self):
        self.options = dict()

    def update(self, update):
        """
        Update the settings for new or existing settings.

        Args:
            update: Dictionary containing settings to be updated.
        """
        self.options.update(update)

    def read(self):
        """
        Method that returns the settings.

        Returns:
            Dictionary containing the options.
        """
        return self.options
