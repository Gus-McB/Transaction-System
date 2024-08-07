from abc import ABC, abstractmethod
import datetime

class ReportInterface(ABC):

    @abstractmethod
    def addReportData(self, clasifiedData: list) -> bool:
        pass

    @abstractmethod
    def getReport(self, startDate: datetime, endDate: datetime, label='') -> list:
        pass