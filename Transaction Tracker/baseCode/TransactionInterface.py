from abc import ABC, abstractmethod
import datetime

class TransactionInterface(ABC):

    @abstractmethod
    def importTransactions(self, filePath: str):
        pass

    @abstractmethod
    def getTransactions(self, startDate: datetime, endDate: datetime):
        pass