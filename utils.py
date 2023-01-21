import time

class Timer:
    def __init__(self) -> None:
        self.start_time = None
        self.end_time = None
        self.has_finished = True

    def start(self):
        self.has_finished = False
        self.start_time = time.time()

    def get_time(self):
        return time.time() - self.start_time

    def end(self):
        self.has_finished = True
        self.end_time = time.time()
        time_elapsed = self.end_time - self.start_time
        self.start_time = None

        return time_elapsed

class InexactFloat(float):
    def __eq__(self, other):
        try:
            return abs(self.real - other) / (0.5 * (abs(self.real) + abs(other))) < 0.001
        except ZeroDivisionError:
            # Could do another inexact comparison here, this is just an example:
            return self.real == other

    def __ne__(self, other):
        return not self.__eq__(other)