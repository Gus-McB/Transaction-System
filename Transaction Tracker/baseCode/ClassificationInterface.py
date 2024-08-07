from abc import ABC, abstractmethod

class ClassificationInterface(ABC):
    
    @abstractmethod
    def clasifyTransactions(transaction: list, patterns: dict) -> list:
        pass
