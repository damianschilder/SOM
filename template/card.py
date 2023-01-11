from abc import ABC, abstractmethod

class Card(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def begin_transaction(self, amount: float) -> int:
        pass

    @abstractmethod
    def end_transaction(self, id: int) -> bool:
        pass

    @abstractmethod
    def cancel_transaction(self, id: int):
        pass
