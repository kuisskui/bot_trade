class InitializationException(Exception):
    """ Initialize failed. """

    def __init__(self, message="Initialize failed"):
        self.message = message
        super().__init__(self.message)
