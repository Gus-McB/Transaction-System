from dataclasses import dataclass
import datetime, TransactionInfo

@dataclass
class ReportData(TransactionInfo.TransactionInfo):
    def __init__(self, date: datetime, description: str, amount: float, label: str):
        super().__init__(date, description, amount)
        self.label = label