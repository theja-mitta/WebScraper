import logging


class ErrorHandler:
    def __init__(self, error):
        self.error = error

    def raise_error(self):
        logging.error(self.error)
        return self.error
