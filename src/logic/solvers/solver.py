from abc import ABC, abstractmethod

class Solver(ABC):
    @abstractmethod
    def solve(self, event):
        pass

    @abstractmethod
    def get_name(self):
        pass