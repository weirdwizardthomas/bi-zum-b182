class NoPathFoundException(Exception):
    def __init__(self, history):
        self.history = history
