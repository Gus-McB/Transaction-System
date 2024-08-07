from dataclasses import dataclass
import datetime

@dataclass
class TransactionInfo:
    def __init__(self, date: datetime, description: str, amount: float):
        self.date = date
        self.description = description
        self.amount = amount